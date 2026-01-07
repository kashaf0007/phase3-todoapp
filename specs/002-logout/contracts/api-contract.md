# API Contract: Logout Button

**Feature**: 002-logout
**Date**: 2025-12-31
**Phase**: Phase 1 - Design

## Overview

The Logout Button feature implements **client-side only logout** using the stateless JWT authentication model. No new backend API endpoints are required or created.

## API Endpoints

### Summary

**New Endpoints**: 0
**Modified Endpoints**: 0
**Deprecated Endpoints**: 0

---

## Client-Side Logout Flow

Since this feature uses stateless JWT authentication, logout is handled entirely on the client side:

### 1. Clear Authentication Data

```typescript
// Remove JWT token from localStorage
localStorage.removeItem("auth_token");

// Remove user data from localStorage
localStorage.removeItem("auth_user");
```

**Result**: User can no longer make authenticated API requests

---

### 2. Clear Application Cache

```typescript
import { useQueryClient } from "@tanstack/react-query";

// Clear all React Query cached data
queryClient.clear();
```

**Result**: No cached task data persists for next user

---

### 3. Navigate to Login Page

```typescript
import { useRouter } from "next/navigation";

// Redirect to login page
router.push("/login");
```

**Result**: User is on unauthenticated page

---

## Existing API Behavior After Logout

After logout, existing API endpoints behave as expected with missing/invalid authentication:

### Authentication Endpoints (Unchanged)

#### POST /api/auth/sign-in/email

**Status**: Unchanged
**Behavior**: User can sign in again after logging out
**Request**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name",
    "emailVerified": false,
    "createdAt": "2025-12-31T10:00:00Z",
    "updatedAt": "2025-12-31T10:00:00Z"
  },
  "session": {
    "token": "eyJhbGci...",
    "expiresAt": "2026-01-07T10:00:00Z"
  }
}
```

---

### Task Endpoints (Unchanged)

All task endpoints return `403 Forbidden` when accessed without valid JWT token (after logout):

#### GET /api/{userId}/tasks

**Status**: Unchanged
**Behavior After Logout**: Returns 403 Forbidden
**Response** (403):
```json
{
  "detail": "Not authenticated"
}
```

#### POST /api/{userId}/tasks

**Status**: Unchanged
**Behavior After Logout**: Returns 403 Forbidden

#### GET /api/{userId}/tasks/{id}

**Status**: Unchanged
**Behavior After Logout**: Returns 403 Forbidden

#### PUT /api/{userId}/tasks/{id}

**Status**: Unchanged
**Behavior After Logout**: Returns 403 Forbidden

#### PATCH /api/{userId}/tasks/{id}/complete

**Status**: Unchanged
**Behavior After Logout**: Returns 403 Forbidden

#### DELETE /api/{userId}/tasks/{id}

**Status**: Unchanged
**Behavior After Logout**: Returns 403 Forbidden

---

## Frontend API Client Behavior

The existing `frontend/src/lib/api.ts` handles 403 errors by redirecting to login:

```typescript
// Existing error handling (unchanged)
if (response.status === 403) {
  if (typeof window !== "undefined") {
    window.location.href = "/login";
  }
  throw new Error("Not authenticated");
}
```

**Result**: If a logged-out user somehow reaches a protected page and attempts an API call, they are redirected to login.

---

## Why No Backend Logout Endpoint?

### Stateless JWT Architecture

The application uses **stateless JWT tokens** where:

1. **Token is self-contained**: Contains all user information (user ID, email, expiration)
2. **Backend doesn't track sessions**: No session table or Redis store
3. **Token remains valid until expiration**: Backend has no revocation mechanism

### Client-Side Logout is Sufficient

Because JWTs are stateless:

- **Security**: Removing token from client prevents user from making authenticated requests
- **Token Expiration**: Tokens are short-lived (7 days as configured in backend)
- **Backend Protection**: Backend still validates JWT signature and expiration on every request
- **Compromised Tokens**: Even if a token is stolen after logout, it will expire soon

### Alternative Considered and Rejected

**Token Blacklist Approach** (Not Implemented):
- Requires backend changes (database table or Redis store)
- Adds complexity to stateless architecture
- Out of scope for Phase II
- Token expiration provides reasonable security window

---

## Security Considerations

### Token Security After Logout

#### What Happens to the JWT After Logout?

1. **Token removed from localStorage**: User's browser no longer has access to it
2. **Token still technically valid**: Backend would accept it if presented (until expiration)
3. **Token cannot be used by user**: No way to access it after localStorage.removeItem()

#### Attack Scenarios

**Scenario 1: User has token memorized/copied**
- **Risk**: Low - tokens are 200+ characters, practically impossible to memorize
- **Mitigation**: Token expiration (7 days maximum)

**Scenario 2: Token stolen before logout**
- **Risk**: Medium - attacker could use token until expiration
- **Mitigation**: Short token lifetime, HTTPS encryption, HTTPOnly cookies (future enhancement)

**Scenario 3: XSS attack reads localStorage**
- **Risk**: High - attacker could steal token
- **Mitigation**: Input sanitization, Content Security Policy (existing)

### Why This is Acceptable for Phase II

1. **Short token lifetime**: 7-day expiration limits damage window
2. **HTTPS required**: Production deployment uses encrypted transport
3. **Scope limitation**: Phase II focuses on basic functionality
4. **Future enhancement**: Token blacklist can be added in Advanced Phase if needed

---

## Error Handling

### Logout Always Succeeds

The logout flow has **no failure modes** that would prevent user from being logged out:

```typescript
export function useLogout() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return async () => {
    // localStorage removal can fail (disabled, full), but we continue
    try {
      if (typeof window !== "undefined") {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("auth_user");
      }
    } catch (error) {
      console.warn("Failed to clear localStorage:", error);
      // Continue anyway - worst case, token is expired so user is safe
    }

    // Cache clearing always succeeds
    queryClient.clear();

    // Navigation always succeeds
    router.push("/login");
  };
}
```

**Principle**: User experience is prioritized - logout must always work even if cleanup fails.

---

## Frontend Route Protection

### AuthGuard Component (Existing)

`frontend/src/components/AuthGuard.tsx` enforces route protection:

```typescript
export function AuthGuard({ children }: AuthGuardProps) {
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [user, loading, router]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null;

  return <>{children}</>;
}
```

**Behavior After Logout**:
1. `localStorage` is cleared
2. Next time `useAuth()` runs, it finds no user
3. `AuthGuard` detects `!user` and redirects to `/login`
4. Protected routes are inaccessible

---

## Testing the Logout Flow

### Manual Test Cases

#### Test 1: Basic Logout
1. Sign in to application
2. Navigate to tasks page
3. Click Logout button
4. **Verify**: Redirected to `/login`
5. **Verify**: localStorage has no `auth_token` or `auth_user`

#### Test 2: Protected Route Access After Logout
1. Complete Test 1 (logged out)
2. Attempt to navigate to `/tasks` manually (type URL)
3. **Verify**: Immediately redirected to `/login`

#### Test 3: Back Button After Logout
1. Complete Test 1 (logged out)
2. Press browser back button
3. **Verify**: Redirected to `/login` (not tasks page)

#### Test 4: Refresh After Logout
1. Complete Test 1 (logged out)
2. Refresh the page
3. **Verify**: Still on `/login`, no session restoration

#### Test 5: Cache Cleared
1. Sign in and view tasks
2. Note task titles
3. Logout
4. Sign in as different user
5. **Verify**: Previous user's tasks not visible

#### Test 6: API Calls After Logout
1. Complete Test 1 (logged out)
2. Use browser dev tools to call `/api/{userId}/tasks`
3. **Verify**: Returns 403 Forbidden

---

## Contract Compliance

### With Constitution

✅ **Principle X**: REST API Contract Compliance
- No API changes made
- All existing endpoints unchanged
- Security model preserved (JWT verification continues)

✅ **Principle VIII**: JWT Security
- Backend continues to verify JWT on all requests
- Client-side token removal does not weaken backend security
- No trust of client-provided data

---

## Summary

**API Changes**: None
**New Endpoints**: 0
**Modified Endpoints**: 0
**Backend Changes**: 0

The Logout Button feature is entirely client-side, relying on:
- localStorage removal to prevent user access to token
- React Query cache clearing to prevent data leakage
- Next.js routing to redirect to login page
- Existing AuthGuard and API error handling for route protection

This approach is consistent with stateless JWT authentication and Phase II scope.
