---
id: "001"
title: "neon-db-persistence-spec"
stage: "spec"
date_iso: "2026-01-23"
surface: "agent"
model: "Qwen Code"
feature: "neon-db-persistence"
branch: "003-neon-db-persistence"
user: "Kashaf Aman"
command: "/sp.specify"
labels: ["database", "persistence", "neon-postgresql", "specification"]
links:
  spec: "../specs/003-neon-db-persistence/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/003-neon-db-persistence/spec.md"
  - "specs/003-neon-db-persistence/checklists/requirements.md"
tests_yaml: []
---

# Feature Specification: Neon PostgreSQL Persistence & Visibility

## Input

```
Database Specification ## Neon PostgreSQL Persistence & Visibility --- ## 1. Objective The objective of this specification is to ensure that **all application data is stored persistently in Neon Serverless PostgreSQL**, and that **all database tables are clearly visible in the Neon dashboard** for verification, debugging, and evaluation purposes. This specification is mandatory for **Phase II** and applies to all backend database operations. --- ## 2. Database Technology Requirement ### 2.1 Approved Database * **Neon Serverless PostgreSQL** (ONLY) ### 2.2 Prohibited Databases * SQLite * Supabase * Firebase * MySQL * Local file-based databases * Any in-memory database > ❗ Any database other than Neon PostgreSQL is a violation of Phase II requirements. --- ## 3. Provisioning Specification ### 3.1 Neon Project Creation * A Neon project MUST be created via the Neon console * The project MUST use PostgreSQL * The database MUST be reachable from the FastAPI backend ### 3.2 Connection String * Neon provides a PostgreSQL connection string * The connection string MUST include: * username * password * host * port * database name --- ## 4. Environment Configuration Specification ### 4.1 Environment Variable The Neon connection string MUST be stored in an environment variable: ``` DATABASE_URL=postgresql://neondb_owner:npg_cIRiT1jD2Xeu@ep-autumn-unit-adb7wino-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require ``` ### 4.2 Usage Rules * The backend MUST read the database URL only from environment variables * No hardcoded credentials are allowed * Frontend MUST NOT access the database directly --- ## 5. Schema Definition Specification ### 5.1 Schema Source of Truth * The database schema MUST be defined in spec files * Code MUST be generated from the schema spec * Any schema change requires spec update first --- ## 6. Tables Specification ### 6.1 tasks Table | Column | Type | Constraints | | ----------- | --------- | --------------------------- | | id | integer | Primary Key, Auto Increment | | user_id | string | Not Null, Indexed | | title | string | Not Null | | description | text | Nullable | | completed | boolean | Default false | | created_at | timestamp | Auto-generated | | updated_at | timestamp | Auto-updated | --- ## 7. ORM Specification (SQLModel) ### 7.1 ORM Requirement * **SQLModel** MUST be used for all database operations * No raw SQL unless strictly necessary ### 7.2 Model Rules * SQLModel models MUST map 1:1 with schema spec * Models MUST include: * table=True * correct column types * indexes as defined --- ## 8. Migration & Table Creation Specification ### 8.1 Table Creation * Tables MUST be created in Neon PostgreSQL * Table creation MAY occur via: * SQLModel metadata creation * Migration tooling (if used) ### 8.2 Visibility Requirement * After creation, tables MUST be visible in: * Neon Dashboard → Tables View --- ## 9. Backend Accessibility Specification * FastAPI backend MUST successfully: * Connect to Neon database * Read data * Write data * Update data * Delete data * Connection failures MUST raise errors --- ## 10. Verification & Acceptance Criteria This specification is considered fulfilled when: * Neon PostgreSQL database is provisioned * DATABASE_URL is correctly configured * `tasks` table exists in Neon * Table structure matches schema spec * Data persists after backend restarts * Backend can access Neon without errors --- ## 11. Claude Code Implementation Instruction When implementing this specification, Claude Code MUST: 1. Read this spec fully 2. Implement SQLModel models 3. Configure database connection using DATABASE_URL 4. Create tables in Neon PostgreSQL 5. Verify table visibility ---
```

## Response

Created a comprehensive feature specification for Neon PostgreSQL persistence and visibility. The specification includes:

1. User scenarios and testing requirements with prioritized user stories
2. Functional requirements covering database connectivity, security, and data persistence
3. Key entities definitions
4. Success criteria with measurable outcomes

The specification ensures all application data is stored persistently in Neon Serverless PostgreSQL and that database tables are visible in the Neon dashboard for verification and debugging purposes. It follows the required schema for the `tasks` table and mandates the use of SQLModel for all database operations.

## Outcome

The specification is complete and ready for the planning phase. A quality checklist was also created to validate the specification's completeness and adherence to requirements.

## Evaluation

The specification successfully translates the database requirements into a user-focused document that describes what the system needs to do rather than how it should be implemented. It includes measurable success criteria and testable requirements while maintaining focus on user value.