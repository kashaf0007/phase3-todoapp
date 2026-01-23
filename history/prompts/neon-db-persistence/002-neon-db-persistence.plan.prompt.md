---
id: "002"
title: "neon-db-persistence-plan"
stage: "plan"
date_iso: "2026-01-23"
surface: "agent"
model: "Qwen Code"
feature: "neon-db-persistence"
branch: "003-neon-db-persistence"
user: "Kashaf Aman"
command: "/sp.plan"
labels: ["database", "persistence", "neon-postgresql", "planning"]
links:
  spec: "../specs/003-neon-db-persistence/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/003-neon-db-persistence/plan.md"
  - "specs/003-neon-db-persistence/research.md"
  - "specs/003-neon-db-persistence/data-model.md"
  - "specs/003-neon-db-persistence/contracts/api-contract.md"
  - "specs/003-neon-db-persistence/quickstart.md"
tests_yaml: []
---

# Implementation Plan: Neon PostgreSQL Setup & Table Visibility

## Input

```
/sp.plan ## Neon PostgreSQL Setup & Table Visibility

---

## 1. Plan Purpose

This plan describes **how the Neon PostgreSQL database will be provisioned, connected, and validated** for Phase II of the Todo Full-Stack Web Application.

The plan ensures:

* Persistent storage using Neon DB
* Schema-driven development
* Tables are visible in the Neon dashboard
* Backend accessibility via FastAPI + SQLModel

---

## 2. Plan Scope

This plan applies to:

* Database provisioning
* Environment configuration
* Schema implementation
* Backend database connectivity
* Verification of table visibility in Neon dashboard

---

## 3. High-Level Strategy

The database will be implemented using a **spec-first approach**, executed entirely through **Claude Code**, with no manual coding.

Execution Flow:

> Write Database Spec → Implement via Claude Code → Apply schema → Verify in Neon Dashboard

---

## 4. Step-by-Step Execution Plan

### Step 1: Provision Neon PostgreSQL Project

**Objective:**
Create a dedicated Neon PostgreSQL database instance.

**Actions:**

1. Log in to Neon Console
2. Create a new Neon project
3. Select PostgreSQL as the database engine
4. Create a primary database instance

**Output:**

* Active Neon PostgreSQL project

---

### Step 2: Obtain Database Connection String

**Objective:**
Retrieve credentials required for backend connectivity.

**Actions:**

1. Open Neon project dashboard
2. Copy PostgreSQL connection string
3. Verify connection string includes:

   * Username
   * Password
   * Host
   * Port
   * Database name

**Output:**

* Valid PostgreSQL connection string

---

### Step 3: Configure Environment Variables

**Objective:**
Securely configure backend database access.

**Actions:**

1. Add connection string to backend environment variables:

```
DATABASE_URL=postgresql://neondb_owner:npg_cIRiT1jD2Xeu@ep-autumn-unit-adb7wino-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

2. Ensure `.env` file is excluded from version control
3. Confirm backend reads database URL only from environment variables

**Output:**

* Secure database configuration

---

### Step 4: Define Database Schema via Specs

**Objective:**
Establish schema as the single source of truth.

**Actions:**

1. Create database schema specification in `/specs/database/`
2. Define `tasks` table structure
3. Define indexes and constraints
4. Review schema spec for completeness

**Output:**

* Approved database schema specification

---

### Step 5: Implement SQLModel Models via Claude Code

**Objective:**
Generate ORM models directly from schema specs.

**Actions:**

1. Reference schema spec using `@specs/database/...`
2. Ask Claude Code to generate SQLModel models
3. Validate model-to-schema alignment

**Output:**

* SQLModel models matching schema spec

---

### Step 6: Apply Table Creation / Migrations

**Objective:**
Create tables inside Neon PostgreSQL.

**Actions:**

1. Configure FastAPI database initialization
2. Apply SQLModel metadata creation or migration logic
3. Start backend service to apply schema

**Output:**

* `tasks` table created in Neon database

---

### Step 7: Verify Neon Dashboard Visibility

**Objective:**
Confirm schema correctness and persistence.

**Actions:**

1. Open Neon Dashboard
2. Navigate to Tables view
3. Verify `tasks` table exists
4. Confirm column structure matches schema spec

**Output:**

* Tables visible in Neon dashboard

---

### Step 8: Backend Connectivity Validation

**Objective:**
Ensure backend can access Neon database.

**Actions:**

1. Run FastAPI backend
2. Perform test CRUD operations
3. Restart backend service
4. Confirm data persistence

**Output:**

* Backend successfully reads/writes data

---

## 5. Risks & Mitigation

| Risk                        | Mitigation                     |
| --------------------------- | ------------------------------ |
| Incorrect connection string | Validate DATABASE_URL format   |
| Tables not visible          | Re-run schema creation step    |
| Data loss                   | Ensure Neon persistent storage |
| Manual schema changes       | Enforce spec-only updates      |

---

## 6. Completion Criteria

This plan is complete when:

* Neon PostgreSQL project exists
* DATABASE_URL is configured
* SQLModel models are implemented
* `tasks` table is visible in Neon dashboard
* Backend accesses Neon successfully

---

## 7. Deliverables

* Neon PostgreSQL database
* Database schema spec
* SQLModel models
* Visible tables in Neon dashboard

---
```

## Response

Created a comprehensive implementation plan for Neon PostgreSQL setup and table visibility. The plan includes:

1. Technical context with known and unknown dependencies
2. Constitution check to ensure compliance with project principles
3. Phase 0 research outlining investigation tasks
4. Phase 1 design with data model, API contracts, and quickstart guide
5. Phase 2 implementation steps with detailed actions
6. Risk mitigation strategies
7. Success criteria and deliverables

Additionally, created supporting documents:
- Research findings documenting key decisions and rationale
- Data model specification detailing the Task entity
- API contracts defining the interface between frontend and backend
- Quickstart guide with step-by-step setup instructions

The plan follows the spec-first approach mandated by the project constitution and ensures all implementation will be done through Claude Code without manual coding.

## Outcome

The implementation plan is complete and ready for the next phase. It provides a clear roadmap for implementing Neon PostgreSQL persistence with all necessary technical details, compliance checks, and supporting documentation.

## Evaluation

The plan successfully translates the feature requirements into a detailed implementation strategy while maintaining compliance with the project constitution. It addresses all required aspects of database provisioning, connection, schema implementation, and verification.