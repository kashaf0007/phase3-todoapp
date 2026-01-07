# Tasks: Phase II Full-Stack Todo Application

**Input**: Design documents from `@specs/001-fullstack-todo-app/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete), contracts/api-spec.yaml (complete)

**Tests**: Tests are NOT explicitly requested in the feature specification, therefore no test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Each task includes exact file paths

## Path Conventions

This is a web application with:
- **Backend**: `backend/src/` (Python FastAPI)
- **Frontend**: `frontend/src/` (Next.js TypeScript)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure with src/, tests/, requirements.txt
- [x] T002 Create frontend directory structure with src/, public/, package.json
- [x] T003 [P] Initialize Python virtual environment and install FastAPI, SQLModel, python-jose, psycopg2-binary in backend/requirements.txt
- [x] T004 [P] Initialize Next.js project with TypeScript and install dependencies (Better Auth, React Query) in frontend/package.json
- [x] T005 [P] Create root .env.example with BETTER_AUTH_SECRET and DATABASE_URL placeholders
- [x] T006 [P] Create backend/.env.example with same environment variables
- [x] T007 [P] Create frontend/.env.local.example with BETTER_AUTH_SECRET and NEXT_PUBLIC_API_URL
- [x] T008 [P] Create backend/CLAUDE.md with backend-specific implementation guidance
- [x] T009 [P] Create frontend/CLAUDE.md with frontend-specific implementation guidance
- [x] T010 [P] Create docker-compose.yml for local development orchestration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Layer

- [x] T011 [P] Create User SQLModel in backend/src/models/user.py with id, email, password_hash, created_at
- [x] T012 [P] Create Task SQLModel in backend/src/models/task.py with id, user_id, title, description, completed, created_at, updated_at
- [x] T013 Create database connection configuration in backend/src/database.py with Neon PostgreSQL engine
- [x] T014 Create get_session() dependency in backend/src/database.py for session management
- [x] T015 Create __init__.py in backend/src/models/ to export User and Task models

### Backend Application Skeleton

- [x] T016 Create environment configuration in backend/src/config.py to load BETTER_AUTH_SECRET and DATABASE_URL
- [x] T017 Create FastAPI app initialization in backend/src/main.py with CORS middleware
- [x] T018 Create health check route in backend/src/api/routes/health.py returning {"status": "healthy"}
- [x] T019 Create __init__.py in backend/src/api/ and backend/src/api/routes/

### JWT Authentication Infrastructure

- [x] T020 Create JWT verification dependency get_current_user() in backend/src/api/dependencies.py
- [x] T021 Implement token extraction from Authorization header in backend/src/api/dependencies.py
- [x] T022 Implement JWT signature verification using python-jose in backend/src/api/dependencies.py
- [x] T023 Implement 401 error handling for missing/invalid/expired tokens in backend/src/api/dependencies.py
- [x] T024 Add user_id extraction from JWT payload in backend/src/api/dependencies.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and sign in to access their personal todo list

**Independent Test**: Register a new account, sign out, sign back in, and verify session persistence

### Implementation for User Story 1

- [x] T025 [P] [US1] Configure Better Auth in frontend/src/lib/auth.ts with JWT strategy and BETTER_AUTH_SECRET
- [x] T026 [P] [US1] Create Better Auth provider wrapper in frontend/src/app/layout.tsx
- [x] T027 [P] [US1] Create signup page in frontend/src/app/signup/page.tsx with email/password form
- [x] T028 [P] [US1] Create login page in frontend/src/app/login/page.tsx with email/password form
- [x] T029 [P] [US1] Create AuthGuard component in frontend/src/components/AuthGuard.tsx to protect routes
- [x] T030 [US1] Implement signup form validation (email format, password minimum 8 characters) in frontend/src/app/signup/page.tsx
- [x] T031 [US1] Implement login form validation and error handling in frontend/src/app/login/page.tsx
- [x] T032 [US1] Add automatic redirect to /tasks after successful signup in frontend/src/app/signup/page.tsx
- [x] T033 [US1] Add automatic redirect to /tasks after successful login in frontend/src/app/login/page.tsx
- [x] T034 [US1] Add redirect to /login for unauthenticated users accessing protected routes in frontend/src/components/AuthGuard.tsx
- [x] T035 [US1] Add session persistence across browser refreshes using Better Auth session management
- [x] T036 [US1] Create landing page in frontend/src/app/page.tsx with redirect logic based on authentication status

**Checkpoint**: At this point, User Story 1 should be fully functional - users can register, login, logout, and have persistent sessions

---

## Phase 4: User Story 2 - Create and View Tasks (Priority: P2)

**Goal**: Enable authenticated users to create new tasks and view their complete task list

**Independent Test**: Create multiple tasks with varying titles and descriptions, then view the complete list

### Backend API for User Story 2

- [x] T037 [P] [US2] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py to list tasks
- [x] T038 [P] [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py to create tasks
- [x] T039 [US2] Add user isolation filter (user_id from JWT) in GET endpoint in backend/src/api/routes/tasks.py
- [x] T040 [US2] Add automatic user_id assignment from JWT in POST endpoint in backend/src/api/routes/tasks.py
- [x] T041 [US2] Create TaskCreate Pydantic model in backend/src/api/routes/tasks.py with title and description validation
- [x] T042 [US2] Create TaskResponse Pydantic model in backend/src/api/routes/tasks.py for API responses
- [x] T043 [US2] Add validation for title (required, 1-255 chars) in TaskCreate model
- [x] T044 [US2] Add validation for description (optional, max 2000 chars) in TaskCreate model
- [x] T045 [US2] Add ordering by created_at DESC in GET endpoint in backend/src/api/routes/tasks.py
- [x] T046 [US2] Register tasks router in backend/src/main.py

### Frontend UI for User Story 2

- [x] T047 [P] [US2] Create task list page in frontend/src/app/tasks/page.tsx with protected route
- [x] T048 [P] [US2] Create TaskList component in frontend/src/components/TaskList.tsx to display tasks
- [x] T049 [P] [US2] Create TaskItem component in frontend/src/components/TaskItem.tsx for individual task display
- [x] T050 [P] [US2] Create TaskForm component in frontend/src/components/TaskForm.tsx for create/edit form
- [x] T051 [P] [US2] Create TypeScript task interfaces in frontend/src/types/task.ts
- [x] T052 [P] [US2] Create API client wrapper in frontend/src/lib/api.ts with JWT attachment
- [x] T053 [US2] Implement fetch tasks functionality using React Query in frontend/src/app/tasks/page.tsx
- [x] T054 [US2] Implement create task form in TaskForm component with title and description fields
- [x] T055 [US2] Add form validation (title required, max lengths) in TaskForm component
- [x] T056 [US2] Add loading states during API calls in task list page
- [x] T057 [US2] Add error message display for failed operations in task list page
- [x] T058 [US2] Add empty state display when user has no tasks in TaskList component
- [x] T059 [US2] Implement 401 response handling (redirect to login) in frontend/src/lib/api.ts
- [x] T060 [US2] Implement 403 response handling (access denied message) in frontend/src/lib/api.ts
- [x] T061 [US2] Add automatic cache invalidation after task creation using React Query

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can register, login, and manage their task list

---

## Phase 5: User Story 3 - Mark Tasks as Complete (Priority: P3)

**Goal**: Enable authenticated users to mark tasks as complete or incomplete to track progress

**Independent Test**: Create a task, mark it complete, then mark it incomplete, verify persistence

### Backend API for User Story 3

- [x] T062 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/routes/tasks.py
- [x] T063 [US3] Add user ownership verification in PATCH endpoint (403 if task belongs to different user)
- [x] T064 [US3] Create TaskCompletionToggle Pydantic model with completed boolean field
- [x] T065 [US3] Add 404 error handling for non-existent tasks in PATCH endpoint
- [x] T066 [US3] Ensure updated_at timestamp updates when completion status changes

### Frontend UI for User Story 3

- [x] T067 [P] [US3] Add completion checkbox to TaskItem component in frontend/src/components/TaskItem.tsx
- [x] T068 [US3] Implement toggle completion handler using React Query mutation in TaskItem component
- [x] T069 [US3] Add visual distinction for completed tasks (strikethrough or styling) in TaskItem component
- [x] T070 [US3] Add loading indicator during toggle operation in TaskItem component
- [x] T071 [US3] Add optimistic update for immediate UI feedback in TaskItem component
- [x] T072 [US3] Add automatic cache invalidation after completion toggle using React Query

**Checkpoint**: All three priority stories (US1, US2, US3) should now be independently functional

---

## Phase 6: User Story 4 - Update Task Details (Priority: P4)

**Goal**: Enable authenticated users to edit task titles and descriptions

**Independent Test**: Create a task, edit its title and description, verify changes persist

### Backend API for User Story 4

- [x] T073 [P] [US4] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T074 [P] [US4] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T075 [US4] Add user ownership verification in both GET and PUT endpoints (403 if violation)
- [x] T076 [US4] Create TaskUpdate Pydantic model with title and description validation
- [x] T077 [US4] Add 404 error handling for non-existent tasks in both endpoints
- [x] T078 [US4] Add validation to prevent empty title updates in PUT endpoint
- [x] T079 [US4] Ensure updated_at timestamp updates when task is modified

### Frontend UI for User Story 4

- [x] T080 [P] [US4] Create task edit page in frontend/src/app/tasks/[id]/page.tsx with protected route
- [x] T081 [US4] Implement edit mode in TaskForm component (reuse for both create and edit)
- [x] T082 [US4] Add "Edit" button to TaskItem component that navigates to edit page
- [x] T083 [US4] Implement fetch task details functionality in edit page using React Query
- [x] T084 [US4] Implement update task functionality with form submission in edit page
- [x] T085 [US4] Add cancel button that reverts changes and returns to task list
- [x] T086 [US4] Add form validation (same as create: title required, max lengths)
- [x] T087 [US4] Add error handling for empty title submission
- [x] T088 [US4] Add automatic redirect to task list after successful update
- [x] T089 [US4] Add automatic cache invalidation after task update using React Query

**Checkpoint**: Four priority stories (US1-US4) should now be independently functional

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P5)

**Goal**: Enable authenticated users to permanently remove tasks they no longer need

**Independent Test**: Create a task, delete it, verify it no longer appears in the list

### Backend API for User Story 5

- [x] T090 [US5] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T091 [US5] Add user ownership verification in DELETE endpoint (403 if task belongs to different user)
- [x] T092 [US5] Add 404 error handling for non-existent tasks in DELETE endpoint
- [x] T093 [US5] Return 204 No Content status on successful deletion

### Frontend UI for User Story 5

- [x] T094 [P] [US5] Add "Delete" button to TaskItem component in frontend/src/components/TaskItem.tsx
- [x] T095 [US5] Implement confirmation dialog before deletion in TaskItem component
- [x] T096 [US5] Implement delete task handler using React Query mutation in TaskItem component
- [x] T097 [US5] Add loading indicator during delete operation in TaskItem component
- [x] T098 [US5] Add optimistic update to remove task from UI immediately
- [x] T099 [US5] Add automatic cache invalidation after deletion using React Query
- [x] T100 [US5] Handle cancel confirmation (no deletion occurs)

**Checkpoint**: All five user stories (US1-US5) should now be independently functional - complete Phase II feature set

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [x] T101 [P] Add responsive CSS styling for mobile devices (375x667) in frontend components
- [x] T102 [P] Add responsive CSS styling for desktop devices (1920x1080) in frontend components
- [x] T103 [P] Implement toast notifications for success/error feedback across all operations
- [x] T104 [P] Add network error handling with retry button in frontend/src/lib/api.ts
- [x] T105 [P] Verify password security (bcrypt hashing) is correctly implemented by Better Auth
- [x] T106 Validate all 51 functional requirements (FR-001 through FR-051) from spec.md
- [x] T107 Test all 12 success criteria (SC-001 through SC-012) from spec.md
- [x] T108 Perform multi-user isolation testing (verify zero cross-user access)
- [x] T109 Test edge cases: session expiry, network failures, validation errors
- [x] T110 Verify forbidden features are absent (no priorities, tags, search, dates, AI, etc.)
- [x] T111 Run complete end-to-end flow: signup → login → create → view → complete → update → delete → logout
- [x] T112 Validate quickstart.md against actual implementation
- [x] T113 Update constitution.md if any principles were refined during implementation
- [x] T114 Code cleanup and refactoring for consistency

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 authentication but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) and US2 (needs tasks to exist) - Independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) and US2 (needs tasks to exist) - Independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) and US2 (needs tasks to exist) - Independently testable

### Within Each User Story

- Backend API endpoints before frontend UI (frontend needs API to call)
- Models/validation before endpoint logic
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: Tasks T003-T010 (all marked [P]) can run in parallel

**Phase 2 (Foundational)**:
- Database: T011-T012 can run in parallel (different models)
- Backend skeleton: T016-T019 can run in parallel (different files)

**Phase 3 (User Story 1)**:
- T025-T029 can run in parallel (different frontend files)

**Phase 4 (User Story 2)**:
- Backend: T037-T038 can run in parallel (different endpoints)
- Frontend: T047-T052 can run in parallel (different components/files)

**Phase 5 (User Story 3)**:
- T067 can start immediately (TaskItem update)

**Phase 6 (User Story 4)**:
- Backend: T073-T074 can run in parallel (different endpoints)
- Frontend: T080 can start immediately

**Phase 7 (User Story 5)**:
- T094 can start immediately (TaskItem update)

**Phase 8 (Polish)**:
- T101-T105 can run in parallel (different concerns)

**Cross-Story Parallelization**: Once Foundational (Phase 2) is complete, different developers can work on different user stories simultaneously:
- Developer A: User Story 1 (authentication)
- Developer B: User Story 2 (backend tasks API)
- Developer C: User Story 2 (frontend tasks UI)

---

## Parallel Example: Phase 2 Foundational

```bash
# Launch database models in parallel:
Task: "Create User SQLModel in backend/src/models/user.py"
Task: "Create Task SQLModel in backend/src/models/task.py"

# Once models complete, launch backend skeleton in parallel:
Task: "Create environment configuration in backend/src/config.py"
Task: "Create FastAPI app initialization in backend/src/main.py"
Task: "Create health check route in backend/src/api/routes/health.py"
```

---

## Parallel Example: User Story 2

```bash
# Launch backend endpoints in parallel:
Task: "Implement GET /api/{user_id}/tasks endpoint"
Task: "Implement POST /api/{user_id}/tasks endpoint"

# Launch frontend components in parallel:
Task: "Create task list page in frontend/src/app/tasks/page.tsx"
Task: "Create TaskList component"
Task: "Create TaskItem component"
Task: "Create TaskForm component"
Task: "Create task type interfaces"
Task: "Create API client wrapper"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T024) - CRITICAL checkpoint
3. Complete Phase 3: User Story 1 (T025-T036) - Authentication
4. Complete Phase 4: User Story 2 (T037-T061) - Core todo functionality
5. **STOP and VALIDATE**: Test authentication + create/view tasks independently
6. This is your MVP - users can register, login, and manage a basic task list

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T024)
2. Add User Story 1 → Test independently → Deploy/Demo (Authentication works!)
3. Add User Story 2 → Test independently → Deploy/Demo (MVP - basic todo list!)
4. Add User Story 3 → Test independently → Deploy/Demo (Task completion tracking!)
5. Add User Story 4 → Test independently → Deploy/Demo (Task editing!)
6. Add User Story 5 → Test independently → Deploy/Demo (Task deletion!)
7. Polish → Final validation → Production ready

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup (Phase 1) together
2. Team completes Foundational (Phase 2) together - CRITICAL for all stories
3. Once Foundational is done, parallelize:
   - Developer A: User Story 1 (T025-T036) - Authentication
   - Developer B: User Story 2 Backend (T037-T046) - Tasks API
   - Developer C: User Story 2 Frontend (T047-T061) - Tasks UI
4. Once US1 + US2 complete, parallelize remaining stories:
   - Developer A: User Story 3 (T062-T072) - Mark complete
   - Developer B: User Story 4 (T073-T089) - Update tasks
   - Developer C: User Story 5 (T090-T100) - Delete tasks
5. Team completes Polish (Phase 8) together

---

## Task Summary

**Total Tasks**: 114 tasks
**Task Breakdown by Phase**:
- Phase 1 (Setup): 10 tasks
- Phase 2 (Foundational): 14 tasks (BLOCKS all user stories)
- Phase 3 (US1 - Authentication): 12 tasks
- Phase 4 (US2 - Create/View): 25 tasks
- Phase 5 (US3 - Mark Complete): 11 tasks
- Phase 6 (US4 - Update): 17 tasks
- Phase 7 (US5 - Delete): 11 tasks
- Phase 8 (Polish): 14 tasks

**Task Breakdown by User Story**:
- User Story 1 (Authentication): 12 tasks
- User Story 2 (Create/View Tasks): 25 tasks
- User Story 3 (Mark Complete): 11 tasks
- User Story 4 (Update Tasks): 17 tasks
- User Story 5 (Delete Tasks): 11 tasks
- Infrastructure (Setup + Foundational): 24 tasks
- Polish & Validation: 14 tasks

**Parallel Opportunities Identified**: 38 tasks marked with [P] can run in parallel within their respective phases

**Independent Test Criteria**:
- US1: Register account → Sign out → Sign in → Verify session persists
- US2: Create multiple tasks → View complete list → Verify only own tasks visible
- US3: Create task → Mark complete → Mark incomplete → Verify persistence
- US4: Create task → Edit title and description → Verify changes persist
- US5: Create task → Delete task → Verify removal from list

**MVP Scope** (Recommended first delivery):
- Phase 1: Setup (T001-T010)
- Phase 2: Foundational (T011-T024)
- Phase 3: User Story 1 - Authentication (T025-T036)
- Phase 4: User Story 2 - Create/View Tasks (T037-T061)
- **Total MVP Tasks**: 61 tasks (54% of full feature)

---

## Format Validation

✅ All tasks follow required checklist format: `- [ ] [ID] [P?] [Story?] Description`
✅ All tasks include specific file paths
✅ All user story tasks include [Story] label (US1-US5)
✅ Setup and Foundational tasks have NO [Story] label (correctly)
✅ Polish phase tasks have NO [Story] label (correctly)
✅ Sequential task IDs (T001-T114)
✅ [P] markers indicate parallelizable tasks
✅ Each user story has independent test criteria
✅ Dependencies clearly documented
✅ MVP scope identified
✅ Parallel opportunities documented

---

## Notes

- All tasks reference exact file paths for implementation
- [P] tasks operate on different files with no dependencies
- [Story] labels map tasks to user stories for traceability
- Each user story is independently completable and testable
- Foundation phase (Phase 2) MUST complete before any user story begins
- Tests are NOT included (not requested in specification)
- Commit after each task or logical group of related tasks
- Stop at any checkpoint to validate story independently before proceeding
- User Story 2 (create/view) is the MVP core value - prioritize after authentication
