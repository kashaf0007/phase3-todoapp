# Research: Phase II Full-Stack Todo Application

**Feature**: 001-fullstack-todo-app
**Date**: 2025-12-30
**Purpose**: Resolve technical unknowns and establish implementation patterns for Better Auth + JWT integration, Neon PostgreSQL connection, and FastAPI/Next.js architecture

## Authentication Flow

### Decision: Better Auth with JWT Token Strategy

**Implementation Approach**:
- Use Better Auth library for Next.js 16+ App Router with JWT token strategy
- Better Auth manages user registration, login, and session handling on frontend
- JWT tokens issued upon successful authentication contain user ID in payload
- Tokens stored in httpOnly cookies for security (automatic by Better Auth)
- Frontend extracts token and attaches to API requests via Authorization header
- Session persistence across browser refreshes handled by Better Auth session management

**Rationale**:
- Better Auth provides production-ready authentication with minimal configuration
- JWT tokens enable stateless backend authorization without session storage
- App Router compatibility ensures future-proof Next.js integration
- httpOnly cookies prevent XSS attacks on token storage
- Widely adopted pattern with strong community support and documentation

**Alternatives Considered**:
1. **NextAuth.js (Auth.js)**: More feature-rich but heavier, includes OAuth providers not needed for Phase II. Better Auth is lighter and sufficient for email/password authentication.
2. **Custom JWT implementation**: Requires manual security handling (password hashing, token generation, refresh logic). Better Auth provides battle-tested security out of the box.
3. **Session-based auth with server-side storage**: Requires backend session store (Redis/database), adds complexity. JWT stateless approach simpler for microservices architecture.

**Configuration Requirements**:
- BETTER_AUTH_SECRET: Shared secret for JWT signing (minimum 32 characters, cryptographically random)
- Token expiration: 7 days (per spec Assumption 2)
- Token payload: { user_id: string, email: string, iat: number, exp: number }

## Backend Authorization

### Decision: python-jose with FastAPI Dependency Injection

**Implementation Approach**:
- Use python-jose library for JWT signature verification (RS256 or HS256 algorithm)
- Create FastAPI dependency `get_current_user()` that:
  1. Extracts JWT from Authorization header (Bearer <token>)
  2. Verifies token signature using BETTER_AUTH_SECRET
  3. Validates token expiration
  4. Extracts user_id from payload
  5. Returns authenticated user object or raises 401 HTTPException
- Apply dependency to all protected route functions: `current_user: User = Depends(get_current_user)`
- Automatically reject requests with missing/invalid/expired tokens (401 Unauthorized)
- Validate user_id from token matches path parameter where applicable (403 Forbidden if mismatch)

**Rationale**:
- python-jose is FastAPI's recommended JWT library, well-documented and maintained
- Dependency injection pattern provides clean, reusable authorization logic
- Automatic 401/403 error handling without boilerplate in every endpoint
- Type-safe user extraction enables IDE autocomplete and validation
- Decouples authentication logic from business logic (Single Responsibility Principle)

**Alternatives Considered**:
1. **PyJWT**: Lower-level library requiring more manual setup. python-jose provides higher-level abstractions better suited for FastAPI.
2. **FastAPI-Users**: Full authentication framework including user management. Overkill for Phase II where Better Auth handles frontend auth; only backend verification needed.
3. **Manual token verification in each endpoint**: Violates DRY principle, error-prone, harder to maintain.

**Error Handling**:
- 401 Unauthorized: Missing Authorization header, invalid token signature, expired token, malformed token
- 403 Forbidden: Valid token but user_id doesn't match resource ownership
- Token verification errors logged (not exposed to client for security)

**Security Considerations**:
- NEVER trust user_id from request body or path parameters - always use JWT payload
- Validate token signature on EVERY request before database queries
- Use constant-time string comparison for user_id validation (timing attack prevention)
- Rotate BETTER_AUTH_SECRET periodically in production (not implemented in Phase II)

## Database Layer

### Decision: Neon Serverless PostgreSQL with SQLModel Sync Engine

**Implementation Approach**:
- Neon connection string format: `postgresql://user:password@host/database?sslmode=require`
- Use SQLModel synchronous engine (not async) for simplicity in Phase II
- Create `get_session()` dependency yielding database sessions
- Session lifecycle: Request start → Database operations → Automatic commit/rollback → Close
- SQLModel handles table creation via `SQLModel.metadata.create_all(engine)`
- Connection pooling via SQLAlchemy engine (default pool size: 5, max overflow: 10)

**Rationale**:
- Neon provides managed PostgreSQL with instant provisioning (no infrastructure setup)
- Serverless scaling matches Phase II's <10 concurrent user requirement
- SQLModel synchronous API simpler than async for Phase II scope (can migrate to async in future phases)
- Automatic session management via dependency injection prevents connection leaks
- Connection pooling provides adequate performance for Phase II scale
- SQLModel's Pydantic integration enables type-safe models with validation

**Alternatives Considered**:
1. **SQLModel async engine**: Requires async/await throughout codebase, adds complexity. Synchronous sufficient for Phase II performance goals (<2s list load, 10 concurrent users).
2. **Raw SQLAlchemy**: More verbose than SQLModel, lacks Pydantic integration. SQLModel provides cleaner API while maintaining SQLAlchemy compatibility.
3. **Local PostgreSQL (docker-compose)**: Requires users to manage database, adds setup complexity. Neon's cloud hosting simplifies onboarding.
4. **Alembic migrations**: Phase II uses simple `create_all()` for table creation. Alembic migrations reserved for future phases when schema evolution needed.

**Connection Configuration**:
```
DATABASE_URL: Neon connection string from environment variable
Engine config:
  - echo=False (no SQL logging in production)
  - pool_pre_ping=True (validate connections before use)
  - pool_size=5 (concurrent connections)
  - max_overflow=10 (additional connections under load)
```

**Session Pattern**:
- Request → `get_session()` → Yield session → Endpoint logic → Automatic commit → Close
- Rollback on exception (FastAPI handles automatically)
- No manual session management in endpoint code

## Environment Configuration

### Decision: Shared .env with BETTER_AUTH_SECRET

**Implementation Approach**:
- Root `.env` file (gitignored) contains BETTER_AUTH_SECRET
- Frontend reads from `.env.local` (Next.js convention): `BETTER_AUTH_SECRET=<value>`
- Backend reads from root `.env` (Python convention): `BETTER_AUTH_SECRET=<value>`
- Use identical secret value in both services for JWT signing/verification
- docker-compose.yml mounts `.env` to both containers
- `.env.example` provides template with placeholder (committed to git)

**Rationale**:
- Single source of truth for shared secrets prevents synchronization errors
- Git-ignored .env files prevent accidental secret commits
- .env.example documents required variables for new developers
- docker-compose simplifies local development with automatic environment injection
- Standard convention across Python (python-dotenv) and Next.js (built-in support)

**Alternatives Considered**:
1. **Separate .env files per service**: Risk of secret mismatch between frontend/backend. Shared secret simplifies synchronization.
2. **Secrets in docker-compose directly**: Harder to manage outside Docker, not suitable for production deployment. .env files work in all environments.
3. **Environment-specific files (.env.dev, .env.prod)**: Adds complexity for Phase II. Single .env with deployment-specific values sufficient.

**Secret Generation**:
```
BETTER_AUTH_SECRET: Cryptographically random 32+ character string
Generation: openssl rand -base64 32
Example: "J8K9L0M1N2O3P4Q5R6S7T8U9V0W1X2Y3Z4"
```

**Production Considerations** (not implemented in Phase II):
- Use managed secret services (AWS Secrets Manager, Azure Key Vault, etc.)
- Rotate secrets periodically
- Never log or expose secrets in error messages

## API Architecture

### Decision: FastAPI with Pydantic Models and Router Separation

**Implementation Approach**:
- Separate routers for logical groupings: `/api/routes/tasks.py`, `/api/routes/health.py`
- Pydantic request models: `TaskCreate(title: str, description: Optional[str])`
- Pydantic response models: `TaskResponse(id: int, user_id: str, title: str, ...)`
- SQLModel entities: `Task` (database model with SQLModel.table = True)
- Automatic validation via Pydantic (400 Bad Request on invalid input)
- Consistent error responses: `{"detail": "Error message"}`
- User isolation enforced in every endpoint via `WHERE user_id = current_user.id`

**Rationale**:
- Router separation enables modular code organization (easier to test and maintain)
- Pydantic models provide automatic request/response validation with type safety
- Separate request/response models prevent leaking internal database fields
- SQLModel entities map directly to database tables with minimal boilerplate
- FastAPI's automatic OpenAPI documentation aids frontend development

**Alternatives Considered**:
1. **Single monolithic router file**: Harder to maintain as endpoints grow. Router separation scales better.
2. **Manual JSON parsing**: Error-prone, no type safety. Pydantic provides automatic validation.
3. **Exposing SQLModel entities directly in responses**: Risks leaking sensitive fields (e.g., password_hash). Separate response models provide explicit control.

**Endpoint Pattern Example**:
```
@router.get("/api/{user_id}/tasks", response_model=List[TaskResponse])
def list_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Ignore user_id from path, use current_user.id from JWT
    tasks = session.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks
```

**Validation Rules**:
- Task title: Required (Pydantic `str`), max length 255 (Pydantic `Field(max_length=255)`)
- Task description: Optional (Pydantic `Optional[str]`), max length 2000
- User ownership: Verify `task.user_id == current_user.id` before update/delete operations
- 403 Forbidden if ownership check fails

**Error Response Format**:
```
{
  "detail": "Human-readable error message",
  "status_code": 400/401/403/404/500
}
```

## Frontend Integration

### Decision: Native Fetch API with JWT Interceptor Pattern

**Implementation Approach**:
- Use native `fetch()` API (no external HTTP library needed)
- Create `apiClient.ts` wrapper with JWT attachment logic
- Extract JWT token from Better Auth session context
- Attach token to all requests: `headers: { Authorization: Bearer ${token} }`
- Handle 401 responses: Clear session, redirect to /login
- Handle 403 responses: Show "Access denied" error message
- Handle network errors: Show user-friendly error, retry button
- Use React Query (TanStack Query) for request state management (loading, error, data)

**Rationale**:
- Native fetch reduces bundle size (no axios dependency)
- Centralized API client ensures consistent JWT attachment across all requests
- React Query provides automatic loading states, error handling, and caching
- 401 auto-redirect prevents users from staying on protected pages after token expiration
- User-friendly error messages improve UX (no raw API errors exposed)

**Alternatives Considered**:
1. **Axios**: More features (interceptors, request cancellation) but heavier bundle. Native fetch sufficient for Phase II needs.
2. **SWR (Vercel's data fetching library)**: Similar to React Query but less mature. React Query has larger ecosystem and better TypeScript support.
3. **Manual fetch in each component**: Violates DRY, inconsistent error handling. Centralized client ensures consistency.

**API Client Pattern**:
```typescript
// lib/api.ts
export async function apiRequest<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const token = await getAuthToken(); // Better Auth session

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options?.headers,
    },
  });

  if (response.status === 401) {
    clearSession();
    router.push('/login');
    throw new Error('Unauthorized');
  }

  if (response.status === 403) {
    throw new Error('Access denied');
  }

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}
```

**React Query Integration**:
- Use `useQuery` for GET requests (automatic caching, refetching)
- Use `useMutation` for POST/PUT/PATCH/DELETE (loading states, error handling, optimistic updates)
- Automatic retry on network failures (3 attempts with exponential backoff)
- Cache invalidation after mutations (refetch task list after create/update/delete)

**Loading States**:
- Skeleton loaders for task list during initial fetch
- Spinner overlays during create/update/delete operations
- Disabled form inputs during submission
- Toast notifications for success/error feedback

## Implementation Priorities

Based on research findings, implementation should proceed in this order:

1. **Database Layer** (Phase 3): SQLModel schemas, Neon connection, session management
2. **Backend Skeleton** (Phase 4): FastAPI app structure, health check, CORS configuration
3. **JWT Verification** (Phase 5): python-jose dependency, get_current_user() function
4. **Task API Endpoints** (Phase 6): All 6 CRUD endpoints with user isolation
5. **Frontend Auth** (Phase 7): Better Auth integration, login/signup pages
6. **Frontend UI** (Phase 8): Task list, create/edit forms, completion toggle
7. **Integration** (Phase 9): API client, error handling, multi-user testing
8. **Validation** (Phase 10): Acceptance criteria testing, security validation

## Technical Risks Revisited

Based on research findings, risk assessments updated:

### Risk 1: Better Auth JWT Format Incompatibility
- **Status**: MITIGATED
- **Finding**: Better Auth JWT tokens follow standard RFC 7519 format, compatible with python-jose
- **Action**: Validate in Phase 5 integration test

### Risk 2: Neon PostgreSQL Connection Issues
- **Status**: MITIGATED
- **Finding**: Neon provides 99.9% uptime SLA, connection pooling handles transient failures
- **Action**: Implement pool_pre_ping=True for connection validation

### Risk 3: User Isolation Bypass Vulnerability
- **Status**: REQUIRES VIGILANCE
- **Finding**: Dependency injection pattern ensures JWT verification on every request
- **Action**: Dedicated security testing in Phase 10, manual code review of all endpoints

### Risk 4: CORS Configuration
- **Status**: MITIGATED
- **Finding**: FastAPI CORS middleware provides simple configuration
- **Action**: Add CORSMiddleware in Phase 4 with frontend origin whitelist

## Research Completion

**Status**: ✅ **COMPLETE**

All technical unknowns resolved. Implementation patterns documented. Ready to proceed to Phase 1 (Design & Contracts).

**Key Decisions Summary**:
- Authentication: Better Auth + JWT tokens
- Backend Authorization: python-jose with FastAPI dependencies
- Database: Neon PostgreSQL + SQLModel sync engine
- Environment: Shared .env with BETTER_AUTH_SECRET
- API Architecture: FastAPI routers + Pydantic models + user isolation
- Frontend: Native fetch + React Query + Better Auth session

**Next Phase**: Generate data-model.md, contracts/api-spec.yaml, quickstart.md
