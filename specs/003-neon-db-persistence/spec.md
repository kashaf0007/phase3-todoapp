# Feature Specification: Neon PostgreSQL Persistence & Visibility

**Feature Branch**: `003-neon-db-persistence`
**Created**: 2026-01-23
**Status**: Draft
**Input**: User description: "Database Specification ## Neon PostgreSQL Persistence & Visibility --- ## 1. Objective The objective of this specification is to ensure that **all application data is stored persistently in Neon Serverless PostgreSQL**, and that **all database tables are clearly visible in the Neon dashboard** for verification, debugging, and evaluation purposes. This specification is mandatory for **Phase II** and applies to all backend database operations. --- ## 2. Database Technology Requirement ### 2.1 Approved Database * **Neon Serverless PostgreSQL** (ONLY) ### 2.2 Prohibited Databases * SQLite * Supabase * Firebase * MySQL * Local file-based databases * Any in-memory database > ❗ Any database other than Neon PostgreSQL is a violation of Phase II requirements. --- ## 3. Provisioning Specification ### 3.1 Neon Project Creation * A Neon project MUST be created via the Neon console * The project MUST use PostgreSQL * The database MUST be reachable from the FastAPI backend ### 3.2 Connection String * Neon provides a PostgreSQL connection string * The connection string MUST include: * username * password * host * port * database name --- ## 4. Environment Configuration Specification ### 4.1 Environment Variable The Neon connection string MUST be stored in an environment variable: ``` DATABASE_URL=postgresql://neondb_owner:npg_TktC9FJmPig5@ep-autumn-recipe-ade5hdh4-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require ``` ### 4.2 Usage Rules * The backend MUST read the database URL only from environment variables * No hardcoded credentials are allowed * Frontend MUST NOT access the database directly --- ## 5. Schema Definition Specification ### 5.1 Schema Source of Truth * The database schema MUST be defined in spec files * Code MUST be generated from the schema spec * Any schema change requires spec update first --- ## 6. Tables Specification ### 6.1 tasks Table | Column | Type | Constraints | | ----------- | --------- | --------------------------- | | id | integer | Primary Key, Auto Increment | | user_id | string | Not Null, Indexed | | title | string | Not Null | | description | text | Nullable | | completed | boolean | Default false | | created_at | timestamp | Auto-generated | | updated_at | timestamp | Auto-updated | --- ## 7. ORM Specification (SQLModel) ### 7.1 ORM Requirement * **SQLModel** MUST be used for all database operations * No raw SQL unless strictly necessary ### 7.2 Model Rules * SQLModel models MUST map 1:1 with schema spec * Models MUST include: * table=True * correct column types * indexes as defined --- ## 8. Migration & Table Creation Specification ### 8.1 Table Creation * Tables MUST be created in Neon PostgreSQL * Table creation MAY occur via: * SQLModel metadata creation * Migration tooling (if used) ### 8.2 Visibility Requirement * After creation, tables MUST be visible in: * Neon Dashboard → Tables View --- ## 9. Backend Accessibility Specification * FastAPI backend MUST successfully: * Connect to Neon database * Read data * Write data * Update data * Delete data * Connection failures MUST raise errors --- ## 10. Verification & Acceptance Criteria This specification is considered fulfilled when: * Neon PostgreSQL database is provisioned * DATABASE_URL is correctly configured * `tasks` table exists in Neon * Table structure matches schema spec * Data persists after backend restarts * Backend can access Neon without errors --- ## 11. Claude Code Implementation Instruction When implementing this specification, Claude Code MUST: 1. Read this spec fully 2. Implement SQLModel models 3. Configure database connection using DATABASE_URL 4. Create tables in Neon PostgreSQL 5. Verify table visibility ---"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Persistent Task Storage (Priority: P1)

As a user of the todo application, I want my tasks to be saved securely in a persistent database so that they remain available even after the application restarts.

**Why this priority**: This is the core functionality of a todo application - without persistent storage, users lose all their data when the application goes down, making the app essentially useless.

**Independent Test**: The system can store tasks in Neon PostgreSQL and retrieve them after restarting the application, demonstrating reliable data persistence.

**Acceptance Scenarios**:

1. **Given** a user creates a new task, **When** the application restarts, **Then** the task remains available to the user
2. **Given** a user modifies a task, **When** the change is saved to the database, **Then** the updated task is retrieved correctly

---

### User Story 2 - Secure Database Connection (Priority: P2)

As a system administrator, I want the application to connect securely to the Neon PostgreSQL database using environment variables so that credentials are not exposed in the codebase.

**Why this priority**: Security is critical for protecting user data and preventing unauthorized access to the database.

**Independent Test**: The application connects to Neon PostgreSQL using only environment variables for credentials, with no hardcoded values in the source code.

**Acceptance Scenarios**:

1. **Given** the application starts up, **When** it attempts to connect to the database, **Then** it uses only the DATABASE_URL environment variable for connection details
2. **Given** the application is deployed, **When** security scanning occurs, **Then** no hardcoded credentials are found in the codebase

---

### User Story 3 - Visible Database Tables (Priority: P3)

As a developer, I want to see all application tables in the Neon dashboard so that I can verify the database schema and troubleshoot issues effectively.

**Why this priority**: Visibility into the database structure is essential for debugging, monitoring, and maintaining the application.

**Independent Test**: The `tasks` table is visible in the Neon dashboard with the correct schema structure.

**Acceptance Scenarios**:

1. **Given** the application has started, **When** I view the Neon dashboard, **Then** I can see the `tasks` table with all specified columns
2. **Given** the application has performed database operations, **When** I check the Neon dashboard, **Then** I can see data in the `tasks` table

---

### Edge Cases

- What happens when the database connection fails during application startup?
- How does the system handle database connection timeouts during operations?
- What occurs when the database is temporarily unavailable during user operations?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST connect to Neon Serverless PostgreSQL using the DATABASE_URL environment variable
- **FR-002**: System MUST store all application data in Neon PostgreSQL database
- **FR-003**: System MUST create a `tasks` table with the specified schema (id, user_id, title, description, completed, created_at, updated_at)
- **FR-004**: System MUST use SQLModel for all database operations
- **FR-005**: System MUST ensure all database tables are visible in the Neon dashboard
- **FR-006**: System MUST prevent hardcoded credentials in the source code
- **FR-007**: System MUST raise appropriate errors when database connections fail
- **FR-008**: System MUST map SQLModel models 1:1 with the schema specification
- **FR-009**: System MUST allow CRUD operations on the `tasks` table
- **FR-010**: System MUST ensure data persists after application restarts

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with properties: id (integer, primary key), user_id (string, not null), title (string, not null), description (text, nullable), completed (boolean, default false), created_at (timestamp), updated_at (timestamp)
- **Database Connection**: Represents the connection to Neon PostgreSQL using environment variables for security

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Neon PostgreSQL database is successfully provisioned and accessible by the application within 5 minutes of setup
- **SC-002**: The `tasks` table exists in Neon with the correct schema structure (all 7 columns with proper types and constraints)
- **SC-003**: Data persists after application restarts - tasks created before restart are available after restart (100% success rate)
- **SC-004**: Database connection failures are handled gracefully with appropriate error messages (no crashes)
- **SC-005**: All database tables are visible in the Neon dashboard for verification and debugging
- **SC-006**: No hardcoded credentials exist in the codebase (verified by security scan)
- **SC-007**: SQLModel is used for all database operations (100% compliance with ORM requirement)