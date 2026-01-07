# Data Model: Logout Button

**Feature**: 002-logout
**Date**: 2025-12-31
**Phase**: Phase 1 - Design

## Overview

The Logout Button feature operates entirely on the client-side and does not introduce any new data entities or modify existing database schemas. This document describes the client-side data structures and state management involved in the logout flow.

## Client-Side Data Structures

### localStorage Keys (Existing)

These keys are already defined in `frontend/src/lib/auth-client.ts` and will be removed during logout:

#### `auth_token`
**Type**: String (JWT token)
**Description**: JSON Web Token for API authentication
**Lifecycle**:
- Created during sign-in/sign-up
- Read on every API request
- **Removed during logout**

**Example Value**:
```json
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
```

#### `auth_user`
**Type**: JSON string (serialized User object)
**Description**: Authenticated user information
**Lifecycle**:
- Created during sign-in/sign-up
- Read to display user info and check authentication state
- **Removed during logout**

**Structure**:
```typescript
{
  id: string;              // UUID of user
  email: string;           // User's email address
  name: string;            // User's display name
  emailVerified: boolean;  // Email verification status
  createdAt: string;       // ISO 8601 timestamp
  updatedAt: string;       // ISO 8601 timestamp
}
```

**Example Value**:
```json
{
  "id": "34cc48f9-d5fd-4372-9192-4cd604dcd499",
  "email": "user@example.com",
  "name": "John Doe",
  "emailVerified": false,
  "createdAt": "2025-12-31T09:47:19.863259",
  "updatedAt": "2025-12-31T09:47:19.863259"
}
```

---

## React Query Cache (Existing - To Be Cleared)

### Task Queries

React Query maintains cached data for task-related API calls. All of these will be cleared during logout using `queryClient.clear()`.

#### Query Key: `["tasks"]`
**Type**: Array of Task objects
**Description**: List of all tasks for the authenticated user
**Source**: `GET /api/{userId}/tasks`
**Cleared**: Yes, via `queryClient.clear()`

**Cached Structure**:
```typescript
Task[] = [
  {
    id: number;
    user_id: string;
    title: string;
    description: string | null;
    completed: boolean;
    created_at: string;  // ISO 8601
    updated_at: string;  // ISO 8601
  },
  // ... more tasks
]
```

#### Query Key: `["task", taskId]`
**Type**: Single Task object
**Description**: Individual task details
**Source**: `GET /api/{userId}/tasks/{id}`
**Cleared**: Yes, via `queryClient.clear()`

**Cached Structure**:
```typescript
{
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}
```

---

## State Management

### Authentication State (React Hook State)

The `useAuth()` hook manages authentication state in React components:

```typescript
{
  user: User | null;        // Current user object or null if not authenticated
  loading: boolean;         // True while checking localStorage
  isAuthenticated: boolean; // Derived: user !== null
}
```

**State Transitions During Logout**:
1. Initial: `{ user: User, loading: false, isAuthenticated: true }`
2. After localStorage clear: Next component re-render will find no user
3. Final: `{ user: null, loading: false, isAuthenticated: false }`

**Note**: The `useAuth()` hook checks localStorage on mount, so clearing localStorage effectively updates this state on the next render or page navigation.

---

## Data Flow During Logout

### Sequence Diagram

```
User                 Component            useLogout Hook       localStorage         QueryClient         Router
  |                      |                      |                    |                    |                |
  |  Click Logout        |                      |                    |                    |                |
  |--------------------->|                      |                    |                    |                |
  |                      | logout()             |                    |                    |                |
  |                      |--------------------->|                    |                    |                |
  |                      |                      | removeItem("auth_token")                |                |
  |                      |                      |------------------------------------------------>|                |
  |                      |                      | removeItem("auth_user")                 |                |
  |                      |                      |------------------------------------------------>|                |
  |                      |                      |                    |  clear()           |                |
  |                      |                      |--------------------------------------------->|                |
  |                      |                      |                    |                    | (All queries   |
  |                      |                      |                    |                    |  removed)      |
  |                      |                      |                    |                    |                |
  |                      |                      | push("/login")     |                    |                |
  |                      |                      |------------------------------------------------------------->|
  |                      |                      |                    |                    |                | Navigate
  |  Redirected to Login |                      |                    |                    |                |---------->
  |<---------------------------------------------------------------------------------------------------------|
```

---

## State Cleanup Checklist

During logout, the following state must be cleared:

- [x] `localStorage.auth_token` - JWT token
- [x] `localStorage.auth_user` - User object
- [x] React Query cache - All task queries (via `queryClient.clear()`)
- [x] Navigation state - Redirect to `/login`
- [ ] ~~Session cookies~~ - Not used (stateless JWT)
- [ ] ~~Backend session~~ - Not applicable (stateless JWT)
- [ ] ~~Component-level state~~ - Automatically cleared on navigation to login

---

## Data Validation

### Pre-Logout Validation
- None required - logout is unconditional
- Works regardless of token validity (expired, invalid, or missing)

### Post-Logout Validation

The following conditions must be true after logout:

1. **localStorage is empty** of auth data:
   ```typescript
   localStorage.getItem("auth_token") === null
   localStorage.getItem("auth_user") === null
   ```

2. **React Query cache is empty**:
   ```typescript
   queryClient.getQueryCache().getAll().length === 0
   ```

3. **User is on login page**:
   ```typescript
   window.location.pathname === "/login"
   ```

4. **Protected routes redirect**:
   - Attempting to navigate to `/tasks` should redirect to `/login`
   - AuthGuard component enforces this

---

## No Database Changes

**Critical Note**: This feature makes **zero database modifications**.

- No new tables
- No new columns
- No data migrations
- No schema changes
- Backend completely unaffected

All logout logic is client-side only, consistent with the stateless JWT authentication approach approved in the specification.

---

## Related Entities (No Changes)

These existing entities are involved in the logout flow but are NOT modified:

### User (Database)
- **Location**: `backend/src/models/user.py`
- **Changes**: None
- **Interaction**: User ID used to construct API URLs, but no user records are updated

### Task (Database)
- **Location**: `backend/src/models/task.py`
- **Changes**: None
- **Interaction**: Task cache is cleared on logout, but no database tasks are modified

---

## Summary

The Logout Button feature is a **pure client-side state management operation**:

- **Removes**: 2 localStorage keys (`auth_token`, `auth_user`)
- **Clears**: React Query cache (all cached API responses)
- **Navigates**: To `/login` page
- **Database Impact**: None
- **Backend Impact**: None
- **New Entities**: None

This minimalist approach aligns with the stateless JWT authentication model and Phase II simplicity principles.
