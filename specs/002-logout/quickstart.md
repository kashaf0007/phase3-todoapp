# Quickstart Guide: Logout Button Implementation

**Feature**: 002-logout
**Branch**: `002-logout`
**Date**: 2025-12-31

## Overview

This guide provides step-by-step instructions for implementing the Logout Button feature. Follow these steps in order to successfully add logout functionality to the Todo application.

---

## Prerequisites

Before starting implementation, ensure:

- ✅ You are on branch `002-logout`
- ✅ Frontend development server is running (`npm run dev` in `frontend/`)
- ✅ You have read the spec: `specs/002-logout/spec.md`
- ✅ You have reviewed the plan: `specs/002-logout/plan.md`
- ✅ All constitutional gates have passed (see plan.md Constitution Check section)

**Check your branch**:
```bash
git branch --show-current
# Should output: 002-logout
```

---

## Implementation Steps

### Step 1: Enhance auth-client.ts with useLogout Hook

**File**: `frontend/src/lib/auth-client.ts`

**Goal**: Create a custom React hook that combines signOut(), cache clearing, and navigation.

**Changes**:

1. Import required dependencies at the top of the file:
```typescript
import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";
```

2. Add the new `useLogout()` hook after the existing `useAuth()` hook:

```typescript
/**
 * React hook for logout functionality
 * Clears authentication data, React Query cache, and navigates to login
 */
export function useLogout() {
  const router = useRouter();
  const queryClient = useQueryClient();

  return async () => {
    // Clear localStorage (with error handling)
    try {
      if (typeof window !== "undefined") {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
      }
    } catch (error) {
      console.warn("Failed to clear localStorage during logout:", error);
      // Continue with logout flow even if localStorage fails
    }

    // Clear React Query cache to prevent data leakage
    queryClient.clear();

    // Navigate to login page
    router.push("/login");
  };
}
```

**Why this approach**:
- Custom hook provides clean API for components
- Encapsulates all logout logic in one place
- Error handling ensures logout always succeeds
- Combines three operations: localStorage cleanup, cache clearing, navigation

**Test**: File should compile without errors after this change.

---

### Step 2: Add Logout Button to Tasks Page

**File**: `frontend/src/app/tasks/page.tsx`

**Goal**: Add a Logout button in the page header that calls our new logout hook.

**Changes**:

1. Import the `useLogout` hook at the top:
```typescript
import { useLogout } from "@/lib/auth-client";
```

2. Replace the entire component with this updated version:

```typescript
export default function TasksPage() {
  const logout = useLogout();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <AuthGuard>
      <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
        <header style={{
          marginBottom: "30px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center"
        }}>
          <h1>My Tasks</h1>
          <button
            onClick={handleLogout}
            style={{
              padding: "10px 20px",
              fontSize: "14px",
              backgroundColor: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Logout
          </button>
        </header>
        <TaskList />
      </div>
    </AuthGuard>
  );
}
```

**What changed**:
- Added `useLogout()` hook invocation
- Created `handleLogout` function to call logout
- Modified header to use flexbox layout
- Added Logout button styled as secondary button (gray)
- Button positioned on right side of header

**Visual result**: Header now shows "My Tasks" on left, "Logout" button on right.

---

### Step 3: Verify Implementation

#### Manual Testing Checklist

Run through these test cases to verify logout functionality:

##### Test 1: Basic Logout Flow
- [ ] Sign in to the application
- [ ] Navigate to `/tasks` page
- [ ] Verify Logout button is visible in header
- [ ] Click Logout button
- [ ] **Expected**: Redirected to `/login` page
- [ ] Open browser DevTools → Application → LocalStorage
- [ ] **Expected**: No `auth_token` or `auth_user` keys present

##### Test 2: Protected Route After Logout
- [ ] After logging out, manually navigate to `/tasks` in address bar
- [ ] **Expected**: Immediately redirected to `/login` page

##### Test 3: Back Button Behavior
- [ ] Sign in, navigate to tasks, then logout
- [ ] Press browser back button
- [ ] **Expected**: Redirected to `/login` (not tasks page)

##### Test 4: Refresh After Logout
- [ ] After logging out, refresh the page
- [ ] **Expected**: Remain on `/login` page (session not restored)

##### Test 5: Cache Clearing
- [ ] Sign in as User A, view tasks, note task titles
- [ ] Logout
- [ ] Sign in as User B
- [ ] **Expected**: User A's tasks not visible (cache cleared)

##### Test 6: Button Visibility
- [ ] When logged out (on `/login` or `/signup` pages), button is not visible ✓
- [ ] When logged in (on `/tasks` page), button is visible ✓

---

### Step 4: Edge Case Testing

Test these edge cases from the specification:

#### Edge Case 1: Logout During Pending Operation
1. Start creating a new task (fill form but don't submit)
2. Click Logout while form is still open
3. **Expected**: Logout succeeds, redirected to login

#### Edge Case 2: Multiple Tabs (Manual)
1. Open tasks page in two browser tabs
2. Logout from Tab 1
3. Switch to Tab 2
4. Try to create a task
5. **Expected**: API call returns 403, user redirected to login in Tab 2

#### Edge Case 3: Expired Token
1. Use browser DevTools to manually expire or corrupt the JWT token in localStorage
2. Click Logout
3. **Expected**: Logout still works (no token validation required)

#### Edge Case 4: localStorage Disabled
1. Open browser in Private/Incognito mode with localStorage disabled (some browsers)
2. Attempt logout
3. **Expected**: Console warning logged, but user still redirected to login

---

## Troubleshooting

### Issue: "useRouter is not a function"

**Cause**: Wrong import source for useRouter

**Fix**: Ensure you're importing from `next/navigation` (not `next/router`):
```typescript
import { useRouter } from "next/navigation"; // Correct for App Router
```

---

### Issue: "queryClient is undefined"

**Cause**: Missing React Query provider in app layout

**Fix**: Verify `frontend/src/app/layout.tsx` has QueryClientProvider:
```typescript
<QueryClientProvider client={queryClient}>
  {children}
</QueryClientProvider>
```

---

### Issue: Logout button not visible

**Cause**: Component might not be rendering or styles not applied

**Debug**:
1. Check React DevTools to see if button is in DOM
2. Verify you're on `/tasks` page (button only shows there)
3. Check browser console for errors

---

### Issue: User not redirected after logout

**Cause**: Navigation not triggering

**Debug**:
1. Check browser console for errors
2. Verify `router.push("/login")` is being called
3. Add `console.log("Logout called")` in logout function

---

### Issue: Tasks still visible after logout

**Cause**: React Query cache not cleared

**Debug**:
1. Open React Query DevTools (if installed)
2. Verify queries are cleared after logout
3. Add `console.log("Cache cleared")` after `queryClient.clear()`

---

## File Checklist

After implementation, verify these files were modified:

- [x] `frontend/src/lib/auth-client.ts` - Added `useLogout()` hook
- [x] `frontend/src/app/tasks/page.tsx` - Added Logout button and handler

**No other files should be modified** for this feature.

---

## Performance Verification

Verify logout meets performance requirements from spec (SC-001):

1. Open browser DevTools → Network tab
2. Clear network log
3. Click Logout button
4. **Measure time from click to login page appearing**
5. **Expected**: Under 2 seconds (typically 100-300ms)

If logout takes longer than 2 seconds, investigate:
- Network latency (shouldn't affect client-side logout)
- React Query cache size (very large caches might take longer to clear)
- Rendering performance (login page loading)

---

## Acceptance Criteria Validation

Before marking this feature complete, verify all acceptance criteria from `spec.md`:

### User Story 1: Secure Logout from Todo List

- [x] **Given** I am logged in and viewing my todo list, **When** I click the Logout button, **Then** I am redirected to the Login page and cannot access the todo list without logging in again

- [x] **Given** I am logged in, **When** I click Logout, **Then** all authentication data (JWT tokens, session data) is cleared from browser storage

- [x] **Given** I have logged out, **When** I try to use the browser's back button, **Then** I am redirected to the Login page instead of seeing my previous todo list

- [x] **Given** I have logged out, **When** I refresh the page, **Then** I remain on the Login page and my session is not restored

### User Story 2: Conditional Logout Button Display

- [x] **Given** I am not logged in, **When** I view the login or signup page, **Then** the Logout button is not visible

- [x] **Given** I am logged in and viewing the todo list, **When** the page loads, **Then** the Logout button is visible and accessible

- [x] **Given** I have just logged in, **When** I am redirected to the todo list, **Then** the Logout button appears immediately

### User Story 3: Session State Reset

- [x] **Given** I am logged in with todo items displayed, **When** I click Logout, **Then** the todo list cache is cleared and not visible to the next user

- [x] **Given** I have logged out, **When** another user logs in on the same device, **Then** they see only their own data with no remnants of my session

- [x] **Given** I am logged in with application state (filters, sort preferences), **When** I logout, **Then** all user-specific state is reset to defaults

---

## Success Criteria Verification

Validate all success criteria from `spec.md` are met:

- [x] **SC-001**: Users can successfully logout with a single button click, with the entire process completing in under 2 seconds

- [x] **SC-002**: 100% of logout attempts result in complete removal of authentication data from browser storage (JWT token and user data)

- [x] **SC-003**: After logout, 100% of attempts to access protected routes result in redirect to Login page

- [x] **SC-004**: After logout, 0% of browser back button or refresh attempts restore the previous authenticated session

- [x] **SC-005**: Logout button is visible only to authenticated users with 100% accuracy

- [x] **SC-006**: Users rate the logout experience as intuitive and reliable (target: 95% satisfaction in user testing)

---

## Next Steps

After completing this implementation:

1. **Run full test suite**: Verify all acceptance criteria pass
2. **Create commit**: Use agentic development workflow
3. **Request review**: If working in team, request code review
4. **Merge to main**: After approval, merge branch to main
5. **Deploy**: Test logout in staging/production environment

---

## Additional Resources

- **Specification**: `specs/002-logout/spec.md`
- **Implementation Plan**: `specs/002-logout/plan.md`
- **Research Decisions**: `specs/002-logout/research.md`
- **Data Model**: `specs/002-logout/data-model.md`
- **API Contract**: `specs/002-logout/contracts/api-contract.md`

---

## Support

If you encounter issues not covered in this guide:

1. Review the specification and plan for clarification
2. Check browser console for error messages
3. Verify all prerequisites are met
4. Test in different browser to rule out browser-specific issues

---

**Implementation Time Estimate**: 15-30 minutes (experienced developer)

**Testing Time Estimate**: 10-15 minutes (manual testing all scenarios)

**Total Feature Time**: 25-45 minutes from start to completion
