# API Contracts: Todo Application with Neon PostgreSQL

## Overview
This document defines the API contracts for the todo application that uses Neon PostgreSQL for data persistence. These contracts ensure consistent communication between the frontend and backend while maintaining the required user isolation and security measures.

## Base URL
```
/api/{user_id}/
```

**Note**: Although the user_id exists in the URL path, the backend MUST derive the real user from JWT token, NOT from the path parameter.

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### 1. List All User Tasks
**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Retrieves all tasks for the authenticated user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id: User identifier from the URL (verification will be done via JWT token)

**Response**:
- Status: 200 OK
- Body: Array of Task objects
```json
[
  {
    "id": 1,
    "user_id": "user123",
    "title": "Sample task",
    "description": "Sample description",
    "completed": false,
    "created_at": "2026-01-23T10:00:00Z",
    "updated_at": "2026-01-23T10:00:00Z"
  }
]
```

**Errors**:
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user trying to access another user's tasks)

### 2. Create New Task
**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Creates a new task for the authenticated user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id: User identifier from the URL (verification will be done via JWT token)

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional description",
  "completed": false
}
```

**Response**:
- Status: 201 Created
- Body: Created Task object
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "New task title",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-01-23T10:00:00Z",
  "updated_at": "2026-01-23T10:00:00Z"
}
```

**Errors**:
- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user trying to create task for another user)

### 3. Get Task Details
**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Description**: Retrieves details of a specific task for the authenticated user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id: User identifier from the URL (verification will be done via JWT token)
- id: Task identifier

**Response**:
- Status: 200 OK
- Body: Task object
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Sample task",
  "description": "Sample description",
  "completed": false,
  "created_at": "2026-01-23T10:00:00Z",
  "updated_at": "2026-01-23T10:00:00Z"
}
```

**Errors**:
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user trying to access another user's task)
- 404: Not Found (task doesn't exist)

### 4. Update Task
**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Description**: Updates an existing task for the authenticated user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id: User identifier from the URL (verification will be done via JWT token)
- id: Task identifier

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

**Response**:
- Status: 200 OK
- Body: Updated Task object
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2026-01-23T10:00:00Z",
  "updated_at": "2026-01-23T11:00:00Z"
}
```

**Errors**:
- 400: Bad Request (invalid input)
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user trying to update another user's task)
- 404: Not Found (task doesn't exist)

### 5. Delete Task
**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Description**: Deletes a specific task for the authenticated user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id: User identifier from the URL (verification will be done via JWT token)
- id: Task identifier

**Response**:
- Status: 204 No Content

**Errors**:
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user trying to delete another user's task)
- 404: Not Found (task doesn't exist)

### 6. Toggle Task Completion
**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Description**: Toggles the completion status of a specific task for the authenticated user

**Headers**:
- Authorization: Bearer `<jwt_token>`

**Path Parameters**:
- user_id: User identifier from the URL (verification will be done via JWT token)
- id: Task identifier

**Response**:
- Status: 200 OK
- Body: Updated Task object
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Sample task",
  "description": "Sample description",
  "completed": true,
  "created_at": "2026-01-23T10:00:00Z",
  "updated_at": "2026-01-23T11:00:00Z"
}
```

**Errors**:
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user trying to toggle another user's task)
- 404: Not Found (task doesn't exist)

## Database Schema Requirements

The API expects the following database schema to be implemented in Neon PostgreSQL:

### Table: tasks
- id (INTEGER, PRIMARY KEY, AUTO_INCREMENT) - Unique identifier
- user_id (VARCHAR, NOT NULL, INDEXED) - Links to the user who owns the task
- title (VARCHAR, NOT NULL) - Task title
- description (TEXT, NULLABLE) - Optional detailed description
- completed (BOOLEAN, DEFAULT FALSE) - Completion status
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) - Creation timestamp
- updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) - Last update timestamp

## Security Requirements

1. JWT Verification: Backend MUST verify JWT signature on every request
2. User Identity Extraction: Backend MUST extract user identity from verified token payload
3. Ownership Verification: All database queries MUST filter by authenticated user ID from token
4. Path Parameter Ignoring: Backend MUST ignore `{user_id}` path parameter and derive user identity exclusively from JWT token
5. Access Control: Users can ONLY read/write their own tasks