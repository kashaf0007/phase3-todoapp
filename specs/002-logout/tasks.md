# Tasks: Logout Button

**Input**: Design documents from `specs/002-logout/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-contract.md

**Tests**: Manual testing only - no automated test tasks required per specification

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/`, `backend/src/` (backend not modified for this feature)
- All modifications are frontend-only

---

## Phase 1: Setup (No Setup Required)

**Purpose**: Project initialization and basic structure

**Status**: ✅ **COMPLETE** - Project already initialized with all required dependencies

- Next.js 16+ App Router ✅
- React 18 ✅
- TanStack React Query v5 ✅
- Custom auth client (auth-client.ts) ✅

**No setup tasks needed** - proceeding directly to implementation.

---

## Phase 2: Foundational (No Foundational Tasks)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Status**: ✅ **COMPLETE** - All foundational infrastructure exists:

- Authentication system (custom auth-client.ts) ✅
- React Query setup (QueryClientProvider in layout) ✅
- Next.js App Router with navigation ✅
- AuthGuard component for route protection ✅

**⚠️ CRITICAL**: No blocking prerequisites - user story implementation can begin immediately

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Secure Logout from Todo List (Priority: P1) 🎯 MVP

**Goal**: Implement core logout functionality that clears authentication data, resets cache, and redirects to login page

**Independent Test**: Can be fully tested by logging in, navigating to the todo list, clicking the Logout button, and verifying that the user is redirected to the login page with all authentication data cleared.

**Acceptance Scenarios**:
1. Click Logout → Redirected to /login and cannot access /tasks without logging in again
2. Click Logout → All authentication data (JWT, user data) cleared from localStorage
3. After logout → Browser back button redirects to /login (not cached tasks page)
4. After logout → Page refresh stays on /login (session not restored)

### Implementation for User Story 1

- [x] T001 [P] [US1] Add useLogout hook to frontend/src/lib/auth-client.ts with imports for useRouter and useQueryClient
- [x] T002 [US1] Implement useLogout hook logic: clear localStorage (try-catch), clear React Query cache, navigate to /login in frontend/src/lib/auth-client.ts
- [x] T003 [US1] Add Logout button to header in frontend/src/app/tasks/page.tsx with flexbox layout (title left, button right)
- [x] T004 [US1] Wire Logout button to useLogout hook and add click handler in frontend/src/app/tasks/page.tsx
- [x] T005 [US1] Style Logout button as secondary (gray background, white text, rounded) in frontend/src/app/tasks/page.tsx

**Manual Testing for User Story 1**:
1. Sign in and verify Logout button appears in tasks page header
2. Click Logout and verify redirect to /login page
3. Open DevTools → Application → localStorage and verify auth_token and auth_user are removed
4. Try to navigate to /tasks manually and verify redirect to /login
5. Press back button after logout and verify redirect to /login
6. Refresh page after logout and verify session not restored

**Checkpoint**: At this point, User Story 1 (core logout) should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conditional Logout Button Display (Priority: P2)

**Goal**: Ensure Logout button only appears when user is authenticated (clean UI)

**Independent Test**: Can be tested by verifying the Logout button is visible when logged in and hidden when not authenticated, without requiring the actual logout functionality to work.

**Acceptance Scenarios**:
1. When logged out (on /login or /signup) → Logout button not visible
2. When logged in (on /tasks) → Logout button visible and accessible
3. Immediately after login → Logout button appears on tasks page

### Implementation for User Story 2

**Status**: ✅ **ALREADY SATISFIED**

This user story is automatically satisfied by User Story 1 implementation because:

- The Logout button is added to `frontend/src/app/tasks/page.tsx` which is wrapped by `<AuthGuard>`
- `AuthGuard` component only renders children when user is authenticated
- Login and signup pages (`/login`, `/signup`) don't include the tasks page component
- Therefore, the button only appears on the authenticated tasks page

**No additional tasks required** - functionality achieved through existing architecture.

**Manual Testing for User Story 2**:
1. While logged out, navigate to /login and verify Logout button not visible
2. While logged out, navigate to /signup and verify Logout button not visible
3. Sign in and verify Logout button appears immediately on /tasks page

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Session State Reset (Priority: P1)

**Goal**: Completely reset session state including React Query cache to prevent data leakage between users

**Independent Test**: Can be tested by logging out and verifying that React Query cache is cleared, no user data persists in memory, and the application state is completely reset.

**Acceptance Scenarios**:
1. Logged in with todos displayed → Logout → Todo list cache cleared (not visible to next user)
2. Logout → Different user logs in → They see only their data (no remnants of previous session)
3. Logged in with application state → Logout → All user-specific state reset to defaults

### Implementation for User Story 3

**Status**: ✅ **ALREADY SATISFIED**

This user story is automatically satisfied by User Story 1 (Task T002) because:

- The `useLogout()` hook implementation includes `queryClient.clear()` which removes ALL cached queries
- This includes the `["tasks"]` query key and all `["task", taskId]` query keys
- localStorage clearing removes all user-specific data
- Navigation to /login resets component state

**No additional tasks required** - functionality achieved by existing Task T002.

**Manual Testing for User Story 3**:
1. Sign in as User A, create/view some tasks, note the task titles
2. Click Logout and verify redirect to /login
3. Sign in as User B
4. Verify User A's tasks are NOT visible (cache was cleared)
5. Create a task as User B and verify only User B's tasks are shown

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Validation

**Purpose**: Final validation and edge case testing

- [x] T006 Verify localStorage clearing works when localStorage is disabled (console warning logged, logout still succeeds)
- [x] T007 Test logout during pending task operation (create/update in progress) - verify logout succeeds
- [x] T008 Test multi-tab scenario: logout from one tab, try to use another tab - verify eventual consistency
- [x] T009 Test logout with expired JWT token - verify logout still works (no validation required)
- [x] T010 Run all acceptance criteria from specs/002-logout/spec.md and verify all pass
- [x] T011 Run quickstart.md validation checklist and verify all items pass
- [x] T012 Verify logout performance: complete in under 2 seconds (measure with DevTools)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: ✅ COMPLETE (no tasks) - Pre-existing infrastructure
- **Foundational (Phase 2)**: ✅ COMPLETE (no tasks) - Pre-existing infrastructure
- **User Story 1 (Phase 3)**: Can start immediately - **5 tasks (T001-T005)**
- **User Story 2 (Phase 4)**: ✅ COMPLETE (no tasks) - Satisfied by US1
- **User Story 3 (Phase 5)**: ✅ COMPLETE (no tasks) - Satisfied by US1
- **Polish (Phase 6)**: Depends on User Story 1 completion - **7 tasks (T006-T012)**

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - Can start immediately - **THIS IS THE ENTIRE IMPLEMENTATION**
- **User Story 2 (P2)**: No additional work - Already satisfied by US1 + existing AuthGuard
- **User Story 3 (P1)**: No additional work - Already satisfied by US1 (queryClient.clear() in T002)

### Within User Story 1

- **T001** (add imports): Can start first
- **T002** (implement hook): Depends on T001 completing
- **T003** (add button UI): Can run in parallel with T001-T002 [P]
- **T004** (wire button): Depends on T002 and T003 completing
- **T005** (style button): Depends on T003, can run parallel with T004 [P]

### Parallel Opportunities

- **T001 and T003** can run in parallel (different concerns in auth-client vs tasks page)
- **T004 and T005** can run in parallel (wiring vs styling - independent)
- All Polish tasks (T006-T012) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Phase 1: Parallel work on hook and UI
Task T001: "Add useLogout hook to frontend/src/lib/auth-client.ts"
Task T003: "Add Logout button to header in frontend/src/app/tasks/page.tsx" [PARALLEL]

# Phase 2: Sequential hook implementation (needs T001)
Task T002: "Implement useLogout hook logic in frontend/src/lib/auth-client.ts"

# Phase 3: Parallel wiring and styling
Task T004: "Wire Logout button to useLogout hook in frontend/src/app/tasks/page.tsx"
Task T005: "Style Logout button in frontend/src/app/tasks/page.tsx" [PARALLEL]

# Polish: All parallel
Task T006-T012: All manual testing tasks can be executed in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. ✅ **Setup**: Already complete (no tasks)
2. ✅ **Foundational**: Already complete (no tasks)
3. **User Story 1**: Complete Tasks T001-T005 (5 tasks)
4. **STOP and VALIDATE**: Run manual tests for User Story 1
5. **Deploy/Demo if ready**: Core logout functionality complete

**Result**: Fully functional logout button with all core features in **5 implementation tasks**.

### Incremental Delivery

1. ✅ **Foundation ready**: Pre-existing infrastructure (Next.js, React Query, auth)
2. **Add User Story 1 (5 tasks)**: → Test independently → **Deploy/Demo (MVP!)**
   - Core logout functionality
   - User Story 2 automatically satisfied (button visibility)
   - User Story 3 automatically satisfied (cache clearing)
3. **Polish (7 tasks)**: → Edge case testing → **Final validation**

### Timeline Estimate

- **User Story 1 Implementation**: 20-30 minutes (5 tasks)
- **Manual Testing**: 10-15 minutes
- **Polish & Validation**: 10-15 minutes
- **Total**: 40-60 minutes from start to complete

---

## Task Summary

**Total Tasks**: 12
- **Setup Phase**: 0 tasks (pre-existing)
- **Foundational Phase**: 0 tasks (pre-existing)
- **User Story 1 (P1)**: 5 tasks ⭐ **CORE MVP**
- **User Story 2 (P2)**: 0 tasks (automatically satisfied)
- **User Story 3 (P1)**: 0 tasks (automatically satisfied)
- **Polish Phase**: 7 tasks (validation & edge cases)

**Implementation Tasks**: 5
**Testing Tasks**: 7 (all manual validation)

**Parallel Opportunities**:
- 2 tasks can run in parallel during US1 implementation (T001+T003, T004+T005)
- All 7 polish tasks can run in parallel

**Critical Path**: T001 → T002 → T004 (3 sequential tasks for core functionality)

**MVP Scope**: User Story 1 only (Tasks T001-T005)

---

## Notes

- All tasks follow required checklist format: `- [ ] [ID] [P?] [Story] Description with file path`
- [P] tasks = different files or independent concerns, no dependencies on incomplete work
- [US1] = User Story 1, [US2] = User Story 2, [US3] = User Story 3
- Each user story is independently completable and testable
- User Stories 2 and 3 require zero additional code - satisfied by US1 + existing architecture
- All testing is manual per specification (no automated test tasks)
- Commit after each task or logical group of parallel tasks
- Stop at checkpoints to validate story independently
- **Efficient Implementation**: Only 5 core tasks needed for complete feature (US2 & US3 achieved "for free")
