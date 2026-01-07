# Implementation Plan: Phase II Full-Stack Todo Application

**Branch**: `001-fullstack-todo-app` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `@specs/001-fullstack-todo-app/spec.md`

**Note**: This plan implements Phase II transformation from console to full-stack multi-user web application with authentication, REST APIs, and persistent storage.

## Summary

Transform existing console-based Todo application into production-grade multi-user Full-Stack Web Application supporting five basic operations (create, view, update, delete, mark complete) with JWT-based authentication, Neon PostgreSQL persistence, and strict user isolation. Implementation follows Database → Backend → Auth → Frontend → Integration → Validation sequence with independent testing at each phase.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript (frontend with Next.js 16+)
**Primary Dependencies**: FastAPI (backend framework), SQLModel (ORM), Better Auth (frontend authentication), Next.js App Router (frontend framework), Neon PostgreSQL Driver (database client)
**Storage**: Neon Serverless PostgreSQL (cloud-hosted, managed via connection string)
**Testing**: pytest (backend API tests), Jest/React Testing Library (frontend component tests)
**Target Platform**: Web application - backend deployed as Python ASGI service, frontend as Next.js static/SSR site
**Project Type**: web (separate backend/ and frontend/ directories in monorepo)
**Performance Goals**: Task list loads <2s for 100 tasks (SC-003), task operations complete <10s (SC-002), support 10+ concurrent users (SC-010)
**Constraints**: Strict user isolation (zero cross-user access), 100% JWT validation enforcement, no forbidden features (priorities, tags, search, dates, AI, RBAC, uploads, notifications)
**Scale/Scope**: Multi-user system (10+ concurrent users minimum), 5 core CRUD operations, 6 REST endpoints, 3 UI pages (login/signup, task list, task edit), 51 functional requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-First Development ✅ PASS
- Specification complete at `@specs/001-fullstack-todo-app/spec.md` (266 lines, 51 requirements)
- All implementation must reference spec explicitly using @specs notation
- No code written before this plan approved

### Principle II: No Manual Coding ✅ PASS
- All code generation will be performed by Claude Code from specifications
- Humans provide specifications and approval only

### Principle III: Agentic Dev Stack Workflow ✅ PASS
- This plan follows required sequence: Spec (complete) → Plan (current) → Tasks (next) → Implement → Validate
- Plan structured as incremental phases with validation gates

### Principle IV: Phase Isolation ✅ PASS
- Only Basic Level features (5 CRUD operations) included in plan
- Forbidden features explicitly excluded in spec (14 items listed)
- No priorities, tags, search, filtering, sorting, dates, AI, chatbot, RBAC, uploads, notifications

### Principle V: Multi-User Authentication ✅ PASS
- Better Auth integration planned for frontend (Phase 5)
- JWT-based backend authorization planned (Phase 3)
- User signup/signin flows included in implementation phases

### Principle VI: Data Persistence ✅ PASS
- Neon Serverless PostgreSQL confirmed as exclusive storage (Phase 1)
- SQLModel as exclusive ORM (Phases 1-4)
- No in-memory or file-based storage planned

### Principle VII: Strict User Isolation ✅ PASS
- Every task associated with user_id foreign key (Phase 1 schema)
- User isolation enforced in all API endpoints (Phase 4)
- Database queries filtered by authenticated user ID

### Principle VIII: JWT Security ✅ PASS
- JWT verification middleware planned (Phase 3)
- User identity extracted from token payload, never from request parameters (Phase 3-4)
- Backend validates token on every request before business logic

### Principle IX: Technology Stack Immutability ✅ PASS
- Frontend: Next.js 16+ App Router ✓
- Backend: Python FastAPI ✓
- ORM: SQLModel ✓
- Database: Neon Serverless PostgreSQL ✓
- Auth: Better Auth + JWT ✓
- Spec System: Spec-Kit Plus ✓

### Principle X: REST API Contract Compliance ✅ PASS
- All 6 required endpoints included in Phase 4:
  - GET /api/{user_id}/tasks
  - POST /api/{user_id}/tasks
  - GET /api/{user_id}/tasks/{id}
  - PUT /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH /api/{user_id}/tasks/{id}/complete
- Security rule enforced: user_id derived from JWT, not path parameter

### Principle XI: Shared Secret Management ✅ PASS
- BETTER_AUTH_SECRET environment variable required (Phase 0 validation, Phase 3 implementation)
- Frontend and backend share identical secret
- No hardcoded secrets in plan

### Principle XII: Monorepo Structure Integrity ✅ PASS
- Plan respects required structure:
  - specs/ contains this plan and design artifacts
  - backend/ will contain FastAPI application
  - frontend/ will contain Next.js application
  - Specs never in code directories

### Principle XIII: CLAUDE.md Hierarchy ✅ PASS
- Root CLAUDE.md exists and has highest precedence
- frontend/CLAUDE.md and backend/CLAUDE.md will be created during implementation
- Plan follows root CLAUDE.md guidance

### Principle XIV: Database Schema Compliance ✅ PASS
- SQLModel exclusive (no raw SQL planned)
- Schema will match @specs/001-fullstack-todo-app/data-model.md (Phase 1)
- Every task includes user_id for ownership enforcement

**GATE STATUS**: ✅ **ALL CHECKS PASS** - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-fullstack-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (complete)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── api-spec.yaml    # OpenAPI 3.0 REST API contract
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Spec quality checklist (complete)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel (Better Auth managed)
│   │   └── task.py          # Task SQLModel with user_id FK
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py  # JWT verification dependency
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py    # Health check endpoint
│   │       └── tasks.py     # 6 task CRUD endpoints
│   ├── database.py          # Neon PostgreSQL connection config
│   ├── config.py            # Environment variables (BETTER_AUTH_SECRET, DATABASE_URL)
│   └── main.py              # FastAPI app initialization
├── tests/
│   ├── test_auth.py         # JWT verification tests
│   ├── test_tasks_api.py    # Task CRUD endpoint tests
│   └── test_user_isolation.py  # Security isolation tests
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── CLAUDE.md                # Backend implementation guidance

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout with Better Auth provider
│   │   ├── page.tsx         # Landing/redirect page
│   │   ├── login/
│   │   │   └── page.tsx     # Login page
│   │   ├── signup/
│   │   │   └── page.tsx     # Signup page
│   │   └── tasks/
│   │       ├── page.tsx     # Task list page
│   │       └── [id]/
│   │           └── page.tsx # Task edit page
│   ├── components/
│   │   ├── TaskList.tsx     # Task list component
│   │   ├── TaskItem.tsx     # Individual task display
│   │   ├── TaskForm.tsx     # Create/edit task form
│   │   └── AuthGuard.tsx    # Protected route wrapper
│   ├── lib/
│   │   ├── api.ts           # API client with JWT attachment
│   │   └── auth.ts          # Better Auth configuration
│   └── types/
│       └── task.ts          # TypeScript task interfaces
├── public/
├── tests/
│   ├── components/          # Component unit tests
│   └── integration/         # E2E flow tests
├── package.json             # Node dependencies
├── .env.local.example       # Frontend environment variables
├── next.config.js           # Next.js configuration
└── CLAUDE.md                # Frontend implementation guidance

docker-compose.yml           # Local development orchestration (backend + frontend + postgres)
.env                        # Root environment variables (gitignored)
.env.example                # Environment variable template
```

**Structure Decision**: Web application structure selected based on spec requirements for separate backend (FastAPI Python) and frontend (Next.js TypeScript) services. Monorepo contains both services with shared environment configuration via BETTER_AUTH_SECRET. Backend exposes REST API consumed by frontend. Database (Neon PostgreSQL) accessed only by backend, never directly from frontend.

## Complexity Tracking

> **No violations** - All constitutional checks pass. No complexity justification required.

## Phase 0: Outline & Research

**Objective**: Resolve all technical unknowns and establish implementation patterns for Better Auth + JWT integration, Neon PostgreSQL connection, and FastAPI/Next.js best practices.

**Prerequisites**: Specification complete (@specs/001-fullstack-todo-app/spec.md)

### Research Tasks

1. **Better Auth Integration with Next.js App Router**
   - Research: Better Auth v1.x configuration for Next.js 16+ App Router
   - Deliverable: JWT token issuance flow, session management approach, environment configuration
   - Output: Document in research.md under "Authentication Flow"

2. **JWT Verification in FastAPI**
   - Research: PyJWT or python-jose library for JWT signature verification
   - Deliverable: Dependency injection pattern for protecting routes, error handling for 401/403
   - Output: Document in research.md under "Backend Authorization"

3. **Neon PostgreSQL Connection with SQLModel**
   - Research: Neon connection string format, SQLModel engine configuration, async vs sync patterns
   - Deliverable: Database session management approach, connection pooling strategy
   - Output: Document in research.md under "Database Layer"

4. **BETTER_AUTH_SECRET Sharing Strategy**
   - Research: Secure environment variable sharing between Next.js and FastAPI in development and production
   - Deliverable: Secret synchronization approach, docker-compose configuration
   - Output: Document in research.md under "Environment Configuration"

5. **Task API Design Patterns**
   - Research: FastAPI route organization, Pydantic request/response models, SQLModel integration
   - Deliverable: Recommended patterns for task CRUD operations with user isolation
   - Output: Document in research.md under "API Architecture"

6. **Frontend-Backend Communication**
   - Research: Next.js API client patterns (fetch vs axios), JWT attachment to headers, error handling
   - Deliverable: Recommended approach for 401 handling and token refresh (if applicable)
   - Output: Document in research.md under "Frontend Integration"

### Research Output

**Deliverable**: `@specs/001-fullstack-todo-app/research.md`

**Format**:
```markdown
# Research: Phase II Full-Stack Todo Application

## Authentication Flow
- **Decision**: [Better Auth configuration approach]
- **Rationale**: [Why this approach chosen]
- **Alternatives Considered**: [Other options evaluated]

## Backend Authorization
- **Decision**: [JWT verification library and pattern]
- **Rationale**: [Why this approach chosen]
- **Alternatives Considered**: [Other options evaluated]

[... repeat for each research area]
```

**Success Criteria**: All NEEDS CLARIFICATION items from Technical Context resolved, implementation patterns documented, no remaining technical unknowns.

## Phase 1: Design & Contracts

**Objective**: Define data models, API contracts, and quickstart guide based on research findings and specification requirements.

**Prerequisites**: research.md complete

### 1.1 Data Model Design

**Input**: @specs/001-fullstack-todo-app/spec.md (Key Entities section, Functional Requirements FR-019 through FR-026)

**Task**: Extract entities and design SQLModel schemas

**Entities**:

1. **User** (managed by Better Auth)
   - id: string (UUID) - Primary key
   - email: string - Unique, used for login
   - password_hash: string - Bcrypt hashed password
   - created_at: datetime - Account creation timestamp
   - tasks: relationship - One-to-many with Task

2. **Task**
   - id: integer - Primary key, auto-increment
   - user_id: string (UUID) - Foreign key to User.id, NOT NULL
   - title: string(255) - Required, task title
   - description: text - Optional, task details
   - completed: boolean - Default false, completion status
   - created_at: datetime - Task creation timestamp
   - updated_at: datetime - Last modification timestamp

**Validation Rules**:
- Task.title: Required (non-empty), max 255 characters (Assumption 7)
- Task.description: Optional, max 2000 characters (Assumption 7)
- Task.user_id: Required, must reference existing User
- Task.completed: Defaults to false
- Task.updated_at: Auto-updated on any field modification

**Relationships**:
- User.tasks → Task (one-to-many)
- Task.user → User (many-to-one via user_id foreign key)

**Indexes**:
- Task.user_id: Index for efficient user-scoped queries (FR-020, Assumption 5)
- User.email: Unique index for authentication lookup (FR-003)

**Deliverable**: `@specs/001-fullstack-todo-app/data-model.md`

### 1.2 API Contract Generation

**Input**: @specs/001-fullstack-todo-app/spec.md (REST API Contract section, FR-027 through FR-036)

**Task**: Generate OpenAPI 3.0 specification for all 6 task endpoints

**Endpoints**:

1. **GET /api/{user_id}/tasks**
   - Summary: List all tasks for authenticated user
   - Security: Bearer JWT required
   - Parameters: user_id (path, ignored - user derived from JWT)
   - Response 200: Array of Task objects
   - Response 401: Unauthorized (missing/invalid token)
   - Response 403: Forbidden (user_id mismatch)

2. **POST /api/{user_id}/tasks**
   - Summary: Create new task
   - Security: Bearer JWT required
   - Parameters: user_id (path, ignored)
   - Request Body: {title: string, description?: string}
   - Response 201: Created Task object
   - Response 400: Bad Request (validation failure)
   - Response 401: Unauthorized
   - Response 403: Forbidden

3. **GET /api/{user_id}/tasks/{id}**
   - Summary: Get task details
   - Security: Bearer JWT required
   - Parameters: user_id (path, ignored), id (path, task ID)
   - Response 200: Task object
   - Response 401: Unauthorized
   - Response 403: Forbidden (task belongs to different user)
   - Response 404: Not Found

4. **PUT /api/{user_id}/tasks/{id}**
   - Summary: Update task title and description
   - Security: Bearer JWT required
   - Parameters: user_id (path, ignored), id (path, task ID)
   - Request Body: {title: string, description?: string}
   - Response 200: Updated Task object
   - Response 400: Bad Request
   - Response 401: Unauthorized
   - Response 403: Forbidden
   - Response 404: Not Found

5. **DELETE /api/{user_id}/tasks/{id}**
   - Summary: Delete task permanently
   - Security: Bearer JWT required
   - Parameters: user_id (path, ignored), id (path, task ID)
   - Response 204: No Content (success)
   - Response 401: Unauthorized
   - Response 403: Forbidden
   - Response 404: Not Found

6. **PATCH /api/{user_id}/tasks/{id}/complete**
   - Summary: Toggle task completion status
   - Security: Bearer JWT required
   - Parameters: user_id (path, ignored), id (path, task ID)
   - Request Body: {completed: boolean}
   - Response 200: Updated Task object
   - Response 401: Unauthorized
   - Response 403: Forbidden
   - Response 404: Not Found

**Security Schemes**:
- BearerAuth: JWT token in Authorization header (Bearer <token>)

**Critical Security Note**: All endpoints MUST derive user identity from JWT token payload, NOT from {user_id} path parameter. Backend must validate authenticated user matches task ownership.

**Deliverable**: `@specs/001-fullstack-todo-app/contracts/api-spec.yaml` (OpenAPI 3.0 format)

### 1.3 Quickstart Guide

**Input**: research.md, data-model.md, api-spec.yaml

**Task**: Create developer quickstart guide for local setup and first task flow

**Content**:
1. Prerequisites (Python 3.11+, Node.js 18+, Neon PostgreSQL account)
2. Environment setup (clone, install dependencies, configure .env)
3. Database initialization (Neon connection string, SQLModel table creation)
4. Backend startup (uvicorn command)
5. Frontend startup (npm run dev)
6. First user flow (signup → login → create task → view list)
7. API testing examples (curl commands with JWT token)
8. Troubleshooting common issues

**Deliverable**: `@specs/001-fullstack-todo-app/quickstart.md`

### 1.4 Agent Context Update

**Task**: Update agent-specific context files with Phase II technology additions

**Command**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Updates**:
- Add FastAPI, SQLModel, Better Auth, JWT to technology context
- Add Neon PostgreSQL connection patterns
- Preserve existing manual context between markers

**Deliverables**:
- Updated agent context file (Claude-specific)
- No manual content removed

### Phase 1 Success Criteria

- [ ] data-model.md complete with User and Task entities, validation rules, indexes
- [ ] contracts/api-spec.yaml complete with all 6 endpoints, security schemes, error responses
- [ ] quickstart.md complete with setup instructions and first flow
- [ ] Agent context updated with Phase II technologies
- [ ] All deliverables reference spec explicitly (@specs notation)
- [ ] No implementation details or code in design documents

## Phase 2: Implementation Planning

**Note**: This phase is handled by `/sp.tasks` command, NOT by `/sp.plan`. The plan ends here.

The `/sp.tasks` command will:
1. Read this plan, spec, data-model, and contracts
2. Generate tasks.md with step-by-step implementation tasks
3. Organize tasks by user story priority (P1 → P5)
4. Break work into testable increments
5. Enable independent delivery of each user story

**Next Command**: `/sp.tasks` (after this plan is approved)

## Implementation Phases (Informational Outline)

*The following is an informational outline. Detailed tasks will be generated by `/sp.tasks` command.*

### Phase 3: Database Layer (Foundation)
- SQLModel schema implementation
- Neon PostgreSQL connection configuration
- Database session management
- Table creation and validation
- User-task relationship enforcement

### Phase 4: Backend Application Skeleton
- FastAPI app initialization
- Project structure setup
- Health check endpoint
- Database session integration
- Development server configuration

### Phase 5: Authentication & JWT Verification
- JWT verification middleware/dependency
- BETTER_AUTH_SECRET configuration
- Token signature validation
- User identity extraction from payload
- 401/403 error handling

### Phase 6: Task CRUD API Endpoints
- GET /api/{user_id}/tasks (list tasks)
- POST /api/{user_id}/tasks (create task)
- GET /api/{user_id}/tasks/{id} (get task)
- PUT /api/{user_id}/tasks/{id} (update task)
- DELETE /api/{user_id}/tasks/{id} (delete task)
- PATCH /api/{user_id}/tasks/{id}/complete (toggle complete)
- User ownership enforcement on all endpoints
- Request/response model validation

### Phase 7: Frontend Authentication Flow
- Better Auth integration and configuration
- Signup page implementation
- Login page implementation
- JWT token storage and retrieval
- Protected route handling
- Session persistence

### Phase 8: Frontend Task UI
- Task list page with completion indicators
- Create task form
- Edit task interface
- Completion toggle interaction
- Loading states during API calls
- Error message display
- Empty state for no tasks

### Phase 9: Frontend-Backend Integration
- API client with JWT attachment
- Authorization header management
- 401 response handling (redirect to login)
- 403 response handling (access denied message)
- Network error handling
- User isolation validation (multi-user testing)

### Phase 10: Validation & Acceptance Testing
- Validate all 51 functional requirements (FR-001 through FR-051)
- Test all 12 success criteria (SC-001 through SC-012)
- Multi-user isolation testing (verify zero cross-user access)
- Edge case testing (session expiry, network failures, validation errors)
- Verify forbidden features absent (no priorities, tags, search, dates, AI, etc.)
- End-to-end flow validation (signup → login → CRUD → logout)

## Dependencies & Execution Order

### Phase Dependencies
1. **Phase 0 (Research)**: No dependencies - can start immediately
2. **Phase 1 (Design)**: Depends on Phase 0 completion (research.md)
3. **Phase 2 (Tasks)**: Handled by /sp.tasks command after plan approval
4. **Phases 3-10**: Will be detailed in tasks.md by /sp.tasks command

### Critical Path
1. Research → 2. Design → 3. Database → 4. Backend Skeleton → 5. Auth → 6. Task API → 7. Frontend Auth → 8. Frontend UI → 9. Integration → 10. Validation

Each phase blocks subsequent phases but internal tasks may be parallelizable (determined by /sp.tasks).

### User Story Mapping to Phases
- **P1 (Authentication)**: Phases 5, 7
- **P2 (Create/View Tasks)**: Phases 3, 4, 6 (POST, GET endpoints), 8 (create form, list view), 9
- **P3 (Mark Complete)**: Phase 6 (PATCH endpoint), 8 (toggle UI), 9
- **P4 (Update Tasks)**: Phase 6 (PUT endpoint), 8 (edit form), 9
- **P5 (Delete Tasks)**: Phase 6 (DELETE endpoint), 8 (delete button), 9

## Risks & Mitigations

### Risk 1: Better Auth JWT Format Incompatibility
- **Impact**: JWT tokens issued by Better Auth may not match FastAPI verification expectations
- **Probability**: Medium
- **Mitigation**: Validate token format in Phase 0 research, create integration test in Phase 5
- **Contingency**: Use Better Auth's JWT customization options or add token transformation layer

### Risk 2: Neon PostgreSQL Connection Issues
- **Impact**: Database unavailable blocks all backend functionality
- **Probability**: Low
- **Mitigation**: Test connection in Phase 1, use connection pooling, implement retry logic
- **Contingency**: Provide local PostgreSQL docker-compose fallback for development

### Risk 3: User Isolation Bypass Vulnerability
- **Impact**: Critical security violation, users accessing other users' tasks
- **Probability**: Low (if JWT verification implemented correctly)
- **Mitigation**: Dedicated security testing phase (Phase 10), code review of all endpoints
- **Contingency**: Add database-level row-level security as defense-in-depth

### Risk 4: CORS Configuration for Frontend-Backend Communication
- **Impact**: Frontend unable to call backend API due to CORS policy
- **Probability**: Medium
- **Mitigation**: Configure CORS in FastAPI during Phase 4, test in Phase 9
- **Contingency**: Use Next.js API routes as proxy if CORS issues persist

## Next Steps

1. **Review this plan** against specification and constitutional requirements
2. **Approve plan** if all requirements met
3. **Proceed to Phase 0**: Generate research.md (handled by this command)
4. **Proceed to Phase 1**: Generate design artifacts (handled by this command)
5. **Run /sp.tasks**: Generate detailed implementation tasks after plan complete
6. **Begin implementation**: Execute tasks sequentially with validation at each step

## Plan Completion Status

- [x] Summary section complete
- [x] Technical Context filled (no NEEDS CLARIFICATION markers)
- [x] Constitution Check complete (14/14 principles validated, all pass)
- [x] Project Structure defined (monorepo with backend/ and frontend/)
- [x] Phase 0 (Research) tasks defined
- [x] Phase 1 (Design) tasks defined with deliverables
- [x] Implementation phases outlined (informational)
- [x] Dependencies and execution order documented
- [x] Risks identified with mitigations
- [x] All references use @specs notation
- [x] No code blocks or implementation details in plan
- [x] All 5 user stories (P1-P5) mapped to phases
- [x] All 6 REST endpoints included
- [x] Security invariants enforced in every phase
- [x] Scope discipline maintained (no forbidden features)

**Plan Status**: ✅ **COMPLETE** - Ready for Phase 0 research execution
