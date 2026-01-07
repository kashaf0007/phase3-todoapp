# Research & Technical Decisions: Logout Button

**Feature**: 002-logout
**Date**: 2025-12-31
**Phase**: Phase 0 - Research

## Overview

This document captures all research and technical decisions made during the planning phase for the Logout Button feature. Since this is a client-side only feature that extends existing authentication infrastructure, minimal research was required.

## Research Areas

### 1. React Query Cache Clearing

**Question**: How to properly clear React Query cache on logout to prevent data leakage between user sessions?

**Decision**: Use `queryClient.clear()` method

**Rationale**:
- TanStack React Query v5 provides `queryClient.clear()` which removes all queries from the cache
- This ensures complete cleanup - no stale data persists for the next user
- Simpler than manually invalidating individual query keys
- Prevents edge cases where new query keys might be added but not included in manual invalidation list

**Alternatives Considered**:
- **Manual invalidation** (`queryClient.invalidateQueries()`) - Requires maintaining a list of all query keys; error-prone as features are added
- **Remove specific queries** (`queryClient.removeQueries()`) - Similar issues to manual invalidation
- **Reset to initial state** (`queryClient.resetQueries()`) - Refetches data which is unnecessary since user is logging out

**Implementation Approach**:
```typescript
// In auth-client.ts
import { useQueryClient } from "@tanstack/react-query";

export function useLogout() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return async () => {
    // Clear localStorage
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);

    // Clear all cached queries
    queryClient.clear();

    // Redirect to login
    router.push("/login");
  };
}
```

---

### 2. Logout Button Placement

**Question**: Where should the Logout button be placed in the UI?

**Decision**: Add Logout button to the tasks page header (within TaskList component or page-level header)

**Rationale**:
- Specification states "Add a Logout button to the Todo List header/navbar"
- Current implementation has a simple header in `tasks/page.tsx` with "My Tasks" title
- TaskList component is the natural place for the button since it's always visible when authenticated
- Follows common UX pattern of having logout in the main application area
- No separate navbar component exists, so header is the appropriate location

**Alternatives Considered**:
- **Create new Navbar component** - Over-engineering for a single button; violates simplicity principle
- **Add to every page** - Redundant; tasks page is the primary authenticated area
- **App layout** - Could work but tasks page is more contextually appropriate per spec

**Implementation Approach**:
- Modify `frontend/src/app/tasks/page.tsx` to add Logout button in the header section
- Style button to be visually distinct (e.g., secondary button, right-aligned)
- Only show when user is authenticated (guaranteed by AuthGuard wrapper)

---

### 3. Navigation After Logout

**Question**: How to handle navigation to login page after logout?

**Decision**: Use Next.js `useRouter` hook with `router.push("/login")`

**Rationale**:
- Next.js App Router provides `useRouter` for programmatic navigation
- `push` method adds to history, allowing user to go back to previous pages (but they'll be redirected by AuthGuard)
- Client-side navigation is fast and doesn't require full page reload
- Existing code already uses this pattern in other components

**Alternatives Considered**:
- **window.location.href** - Causes full page reload; slower user experience
- **router.replace("/login")** - Prevents back button; doesn't match natural browser behavior
- **Redirect component** - Requires rendering, less direct than imperative navigation

**Implementation Approach**:
```typescript
import { useRouter } from "next/navigation";

const router = useRouter();
await signOut();
router.push("/login");
```

---

### 4. Hook vs Function Approach

**Question**: Should logout logic be a React hook or a simple function?

**Decision**: Create a `useLogout()` custom hook that returns a logout function

**Rationale**:
- Needs access to React Query's `queryClient` (requires `useQueryClient` hook)
- Needs access to Next.js router (requires `useRouter` hook)
- Custom hook provides clean API: `const logout = useLogout()`
- Encapsulates all logout logic in one place
- Hooks can only be called from React components, which matches our use case

**Alternatives Considered**:
- **Plain async function** - Cannot access React hooks (queryClient, router) directly
- **Enhanced signOut()** - Would need to pass dependencies as parameters; less clean
- **Context-based logout** - Over-engineering for this simple feature

**Implementation Approach**:
```typescript
export function useLogout() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return async () => {
    // Existing signOut logic
    if (typeof window !== "undefined") {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    }

    // New: Clear React Query cache
    queryClient.clear();

    // New: Navigate to login
    router.push("/login");
  };
}
```

---

### 5. Multi-Tab Logout Handling

**Question**: How to handle logout when user has multiple browser tabs open?

**Decision**: Accept eventual consistency - other tabs will realize user is logged out when they try to make API requests

**Rationale**:
- Cross-tab communication (localStorage events, BroadcastChannel API) is complex and out of scope for Phase II
- Current AuthGuard already checks localStorage on mount - other tabs will redirect to login when navigated
- API requests in other tabs will get 401 errors after token is cleared, triggering redirect in api.ts
- Specification doesn't require instant cross-tab logout
- Edge case listed in spec but not a blocking requirement

**Alternatives Considered**:
- **localStorage 'storage' event** - Could work but requires event listeners in all components; adds complexity
- **BroadcastChannel API** - Modern but not supported in all browsers; over-engineering
- **Polling localStorage** - Performance overhead; unnecessary

**Implementation Notes**:
- Existing error handling in `api.ts` already redirects to `/login` on 401 errors
- This provides eventual consistency - other tabs will be logged out when they try to use the API
- Good enough for Phase II scope

---

### 6. Expired Token Handling

**Question**: How to handle logout if JWT token is already expired?

**Decision**: Logout flow works identically regardless of token expiration state

**Rationale**:
- Client-side logout doesn't check token validity - just removes it
- If token is expired, user is effectively already logged out from backend perspective
- Frontend cleanup (clear localStorage, clear cache, navigate) is still necessary
- No additional logic needed

**Implementation**: No special handling required. Existing logout flow is sufficient.

---

### 7. localStorage Disabled/Full Handling

**Question**: How to handle edge case where localStorage is disabled or full?

**Decision**: Wrap localStorage operations in try-catch; continue with rest of logout flow

**Rationale**:
- Spec lists this as an edge case to consider
- Failure to clear localStorage shouldn't prevent navigation to login page
- Private browsing mode or disabled storage is rare but possible
- Graceful degradation: user still gets logged out even if storage cleanup fails

**Implementation Approach**:
```typescript
export function useLogout() {
  const queryClient = useQueryClient();
  const router = useRouter();

  return async () => {
    // Try to clear localStorage, but don't fail logout if it errors
    try {
      if (typeof window !== "undefined") {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
      }
    } catch (error) {
      console.warn("Failed to clear localStorage:", error);
      // Continue with logout flow anyway
    }

    // Always clear cache and navigate
    queryClient.clear();
    router.push("/login");
  };
}
```

---

## Best Practices Applied

### React Query Cache Management
- Use `queryClient.clear()` for complete cache cleanup
- Call it synchronously before navigation to ensure immediate effect
- No refetching needed since user is leaving authenticated area

### Next.js Navigation Patterns
- Use `useRouter` from `next/navigation` (App Router)
- Use `push()` for natural browser history behavior
- Call after state cleanup for correct execution order

### Error Handling
- Wrap localStorage operations in try-catch
- Log warnings but don't block logout flow
- Prioritize user experience over perfect cleanup

### React Hooks Composition
- Custom `useLogout()` hook combines `useQueryClient` and `useRouter`
- Returns simple async function for easy invocation
- Encapsulates all logout logic in one reusable place

---

## Dependencies Required

### Existing (No New Installations)
- `@tanstack/react-query` - Already installed (v5)
- `next/navigation` - Built into Next.js 16+
- `react` - Already installed

### New
- None - All required dependencies already present in the project

---

## Security Considerations

### Token Removal
- Remove both `auth_token` and `auth_user` from localStorage
- No backend invalidation needed (stateless JWT approach per spec)
- Token remains valid until expiration, but user cannot access it

### Cache Clearing
- Critical for multi-user device scenarios
- Prevents next user from seeing previous user's tasks
- `queryClient.clear()` removes all cached data

### Route Protection
- Existing `AuthGuard` component checks localStorage on mount
- After logout, all protected routes redirect to `/login`
- Back button and refresh both trigger AuthGuard check

---

## Open Questions

None - All technical decisions resolved during research phase.

---

## Summary

The Logout Button feature requires minimal technical research as it extends existing authentication infrastructure. Key decisions:

1. **Cache Clearing**: Use `queryClient.clear()` for complete cleanup
2. **Button Placement**: Add to tasks page header
3. **Navigation**: Use `useRouter().push("/login")`
4. **Hook Pattern**: Custom `useLogout()` hook for clean API
5. **Multi-tab**: Accept eventual consistency via existing API error handling
6. **Edge Cases**: Graceful degradation with try-catch for localStorage errors

All decisions align with Phase II principles, use existing dependencies, and maintain simplicity.
