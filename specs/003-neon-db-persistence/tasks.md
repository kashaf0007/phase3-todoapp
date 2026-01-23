# Tasks: Neon PostgreSQL Setup & Table Visibility

## Feature Overview

This feature implements persistent storage for the Todo application using Neon Serverless PostgreSQL. The implementation ensures all application data is stored persistently and that database tables are visible in the Neon dashboard for verification and debugging.

**Feature Branch**: `003-neon-db-persistence`

## Implementation Strategy

The implementation follows a phased approach:
1. **Setup Phase**: Initialize project structure and dependencies
2. **Foundational Phase**: Implement core database infrastructure
3. **User Story Phases**: Implement features in priority order (P1, P2, P3)
4. **Polish Phase**: Cross-cutting concerns and final validation

**MVP Scope**: User Story 1 (Persistent Task Storage) provides core functionality with data persistence.

## Phase 1: Setup

**Goal**: Prepare the development environment and initialize project dependencies.

**Independent Test**: Project structure is set up with all necessary dependencies installed.

**Tasks**:

- [X] T001 Create backend directory structure if not exists
- [X] T002 Install SQLModel and related dependencies in pyproject.toml
- [X] T003 [P] Install psycopg2-binary for PostgreSQL connectivity
- [X] T004 [P] Install python-dotenv for environment variable management
- [X] T005 Create .env file with DATABASE_URL placeholder in backend/
- [X] T006 Add .env to .gitignore to prevent credential exposure
- [X] T007 Create database configuration module at backend/database/

## Phase 2: Foundational

**Goal**: Implement core database infrastructure including connection management and model definitions.

**Independent Test**: Database connection can be established and Task model is properly defined.

**Tasks**:

- [X] T008 [P] Create database connection utility at backend/database/connection.py
- [X] T009 [P] Define Task model at backend/models/task.py following SQLModel specification
- [X] T010 Create database initialization function at backend/database/init_db.py
- [X] T011 [P] Configure environment variable loading in main application
- [X] T012 [P] Implement error handling for database connection failures
- [X] T013 [P] Create database session management utilities

## Phase 3: User Story 1 - Persistent Task Storage (Priority: P1)

**Goal**: Enable users to save tasks securely in a persistent database so they remain available after application restarts.

**Independent Test**: The system can store tasks in Neon PostgreSQL and retrieve them after restarting the application, demonstrating reliable data persistence.

**Acceptance Scenarios**:
1. Given a user creates a new task, When the application restarts, Then the task remains available to the user
2. Given a user modifies a task, When the change is saved to the database, Then the updated task is retrieved correctly

**Tasks**:

- [X] T014 [P] [US1] Create Task CRUD service at backend/services/task_service.py
- [X] T015 [P] [US1] Implement create_task function with user_id association
- [X] T016 [P] [US1] Implement get_tasks_for_user function with proper filtering
- [X] T017 [P] [US1] Implement get_task_by_id function with user ownership check
- [X] T018 [P] [US1] Implement update_task function with user ownership validation
- [X] T019 [P] [US1] Implement delete_task function with user ownership validation
- [X] T020 [P] [US1] Implement toggle_task_completion function with user ownership validation
- [X] T021 [US1] Create database session dependency for FastAPI at backend/database/deps.py
- [X] T022 [US1] Update FastAPI application to initialize database tables on startup
- [X] T023 [US1] Test data persistence by creating a task and restarting the application

## Phase 4: User Story 2 - Secure Database Connection (Priority: P2)

**Goal**: Ensure the application connects securely to the Neon PostgreSQL database using environment variables without exposing credentials in the codebase.

**Independent Test**: The application connects to Neon PostgreSQL using only environment variables for credentials, with no hardcoded values in the source code.

**Acceptance Scenarios**:
1. Given the application starts up, When it attempts to connect to the database, Then it uses only the DATABASE_URL environment variable for connection details
2. Given the application is deployed, When security scanning occurs, Then no hardcoded credentials are found in the codebase

**Tasks**:

- [X] T024 [P] [US2] Audit codebase for any hardcoded database credentials
- [X] T025 [P] [US2] Create database configuration validation at backend/config/db_config.py
- [X] T026 [P] [US2] Implement secure connection string parsing
- [X] T027 [US2] Add startup validation to verify DATABASE_URL is set
- [X] T028 [US2] Create security scanning script to detect hardcoded credentials
- [X] T029 [US2] Document database security practices in README.md

## Phase 5: User Story 3 - Visible Database Tables (Priority: P3)

**Goal**: Make all application tables visible in the Neon dashboard for verification, debugging, and troubleshooting.

**Independent Test**: The `tasks` table is visible in the Neon dashboard with the correct schema structure.

**Acceptance Scenarios**:
1. Given the application has started, When I view the Neon dashboard, Then I can see the `tasks` table with all specified columns
2. Given the application has performed database operations, When I check the Neon dashboard, Then I can see data in the `tasks` table

**Tasks**:

- [X] T030 [P] [US3] Verify table creation by checking Neon dashboard
- [X] T031 [P] [US3] Validate table schema matches specification in Neon dashboard
- [X] T032 [P] [US3] Create sample data insertion script for testing visibility
- [X] T033 [US3] Document how to access and verify tables in Neon dashboard
- [X] T034 [US3] Create database schema verification tests
- [X] T035 [US3] Add logging to confirm table creation during application startup

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Final validation, error handling, and cross-cutting concerns.

**Independent Test**: All functionality works together and meets success criteria.

**Tasks**:

- [X] T036 [P] Implement comprehensive error handling for all database operations
- [X] T037 [P] Add database connection health check endpoint
- [X] T038 [P] Create database backup and recovery documentation
- [X] T039 [P] Implement connection pooling for improved performance
- [X] T040 [P] Add database query logging for debugging
- [X] T041 [P] Create comprehensive test suite for database operations
- [X] T042 [P] Update documentation with database setup instructions
- [X] T043 [P] Perform end-to-end testing of all user stories
- [X] T044 [P] Verify all success criteria from specification are met
- [X] T045 [P] Clean up temporary files and finalize implementation

## Dependencies

### User Story Completion Order
1. US1 (P1) - Persistent Task Storage: Foundation for all other stories
2. US2 (P2) - Secure Database Connection: Security layer on top of persistence
3. US3 (P3) - Visible Database Tables: Verification and monitoring

### Critical Path
- T001 → T002 → T008 → T009 → T010 → T014 → T015 → T022 (Essential for MVP)

## Parallel Execution Examples

### Per User Story
- **US1**: T014-T020 can be developed in parallel by different developers working on different CRUD operations
- **US2**: T024-T026 can be developed in parallel with security audits and configuration validation
- **US3**: T030-T032 can be executed in parallel with verification and testing tasks

### Across Stories
- T036-T045 can be worked on in parallel after foundational elements are complete
- Database connection (US2) can be implemented in parallel with CRUD operations (US1) once the model is defined