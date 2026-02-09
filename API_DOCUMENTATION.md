# Project Management API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

This API uses JWT (JSON Web Token) authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Table of Contents
1. [Authentication](#authentication-endpoints)
2. [Users](#user-endpoints)
3. [Workspaces](#workspace-endpoints)
4. [Projects](#project-endpoints)
5. [Tasks](#task-endpoints)

---

## Authentication Endpoints

### 1. Obtain JWT Token
**POST** `/auth/token/`

Authenticate and receive access and refresh tokens.

**Permission:** Public

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (201 Created):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 2. Refresh JWT Token
**POST** `/auth/token/refresh/`

Obtain a new access token using a refresh token.

**Permission:** Public

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## User Endpoints

### 1. Register User
**POST** `/auth/register/`

Create a new user account.

**Permission:** Public

**Request Body:**
```json
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "avatar": "file (optional)"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "username": "string",
    "email": "user@example.com",
    "avatar": "http://localhost:8000/media/avatars/filename.jpg"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "username": ["This field may not be blank."],
  "email": ["Enter a valid email address."]
}
```

---

### 2. List All Users
**GET** `/auth/`

Retrieve a list of all registered users.

**Permission:** Authenticated

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": "http://localhost:8000/media/avatars/john.jpg",
    "date_joined": "2026-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "username": "jane_smith",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "avatar": null,
    "date_joined": "2026-01-20T14:20:00Z"
  }
]
```

---

### 3. Get User Details
**GET** `/auth/<user_id>/`

Retrieve details of a specific user.

**Permission:** Authenticated

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "http://localhost:8000/media/avatars/john.jpg",
  "date_joined": "2026-01-15T10:30:00Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "User not found"
}
```

---

### 4. Update User
**PUT** `/auth/<user_id>/update/`

Update user information.

**Permission:** Authenticated

**Request Body:**
```json
{
  "username": "string (optional)",
  "email": "user@example.com (optional)",
  "avatar": "file (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe_updated",
  "email": "john_updated@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "http://localhost:8000/media/avatars/john_new.jpg",
  "date_joined": "2026-01-15T10:30:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Error message details"
}
```

---

### 5. Delete User
**DELETE** `/auth/<user_id>/delete/`

Delete a user account.

**Permission:** Authenticated

**Response (204 No Content):**
```
No content returned
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Failed to delete user."
}
```

---

## Workspace Endpoints

### 1. List All Workspaces
**GET** `/workspaces/`

Retrieve a list of all workspaces.

**Permission:** Authenticated

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Development Team",
    "description": "Main development workspace",
    "created_at": "2026-01-10T09:00:00Z"
  },
  {
    "id": 2,
    "name": "Marketing Team",
    "description": "Marketing projects workspace",
    "created_at": "2026-01-12T10:00:00Z"
  }
]
```

---

### 2. List User's Workspaces
**GET** `/workspaces/me/`

Retrieve workspaces where the authenticated user is a member.

**Permission:** Authenticated

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Development Team",
    "description": "Main development workspace",
    "created_at": "2026-01-10T09:00:00Z"
  }
]
```

---

### 3. Create Workspace
**POST** `/workspaces/create/`

Create a new workspace.

**Permission:** Authenticated

**Request Body:**
```json
{
  "name": "string",
  "description": "string (optional)"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "New Workspace",
  "description": "A new workspace for the team",
  "created_at": "2026-02-09T12:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "name": ["This field is required."]
}
```

---

### 4. Get Workspace Details
**GET** `/workspaces/<workspace_id>/`

Retrieve details of a specific workspace.

**Permission:** Authenticated

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Development Team",
  "description": "Main development workspace",
  "created_at": "2026-01-10T09:00:00Z"
}
```

---

### 5. Update Workspace
**PUT** `/workspaces/<workspace_id>/update/`

Update workspace information.

**Permission:** Authenticated

**Request Body:**
```json
{
  "name": "string",
  "description": "string (optional)"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Updated Workspace Name",
  "description": "Updated description",
  "created_at": "2026-01-10T09:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Error message details"
}
```

---

### 6. Delete Workspace
**DELETE** `/workspaces/<workspace_id>/delete/`

Delete a workspace.

**Permission:** Authenticated

**Response (204 No Content):**
```
No content returned
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Failed to delete workspace."
}
```

---

## Project Endpoints

### 1. List Projects
**GET** `/projects/`

Retrieve a list of all projects, optionally filtered by workspace.

**Permission:** Authenticated

**Query Parameters:**
- `workspace_id` (optional): Filter projects by workspace ID

**Examples:**
- Get all projects: `/projects/`
- Get projects in a workspace: `/projects/?workspace_id=1`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Website Redesign",
    "description": "Complete website redesign project",
    "workspace": 1,
    "deadline": "2026-03-15T23:59:59Z",
    "created_at": "2026-01-20T10:00:00Z",
    "updated_at": "2026-02-01T14:30:00Z"
  },
  {
    "id": 2,
    "name": "Mobile App Development",
    "description": "New mobile application",
    "workspace": 1,
    "deadline": "2026-06-30T23:59:59Z",
    "created_at": "2026-01-25T11:00:00Z",
    "updated_at": "2026-01-25T11:00:00Z"
  }
]
```

---

### 2. Create Project
**POST** `/projects/create/`

Create a new project.

**Permission:** Authenticated

**Request Body:**
```json
{
  "name": "string",
  "workspace": 1,
  "description": "string (optional)",
  "deadline": "2026-12-31T23:59:59Z (optional)"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "New Project",
  "description": "Project description",
  "workspace": 1,
  "deadline": "2026-12-31T23:59:59Z",
  "created_at": "2026-02-09T12:00:00Z",
  "updated_at": "2026-02-09T12:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "name": ["This field is required."],
  "workspace": ["This field is required."]
}
```

---

### 3. Get Project Details
**GET** `/projects/<project_id>/`

Retrieve details of a specific project.

**Permission:** Authenticated

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Website Redesign",
  "description": "Complete website redesign project",
  "workspace": 1,
  "deadline": "2026-03-15T23:59:59Z",
  "created_at": "2026-01-20T10:00:00Z",
  "updated_at": "2026-02-01T14:30:00Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Project not found"
}
```

---

### 4. Update Project
**PUT** `/projects/<project_id>/update/`

Update project information.

**Permission:** Authenticated

**Request Body:**
```json
{
  "name": "string",
  "description": "string (optional)",
  "deadline": "2026-12-31T23:59:59Z (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Updated Project Name",
  "description": "Updated description",
  "workspace": 1,
  "deadline": "2026-04-15T23:59:59Z",
  "created_at": "2026-01-20T10:00:00Z",
  "updated_at": "2026-02-09T12:30:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Error message details"
}
```

---

### 5. Delete Project
**DELETE** `/projects/<project_id>/delete/`

Delete a project.

**Permission:** Authenticated

**Response (204 No Content):**
```
No content returned
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Failed to delete project."
}
```

---

## Task Endpoints

### 1. List Tasks
**GET** `/tasks/`

Retrieve a list of all tasks, optionally filtered by project or user.

**Permission:** Authenticated

**Query Parameters:**
- `project_id` (optional): Filter tasks by project ID
- `user_id` (optional): Filter tasks assigned to the authenticated user

**Examples:**
- Get all tasks: `/tasks/`
- Get tasks in a project: `/tasks/?project_id=1`
- Get user's assigned tasks: `/tasks/?user_id=1`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Design homepage",
    "description": "Create mockups for the new homepage",
    "project": 1,
    "assignees": [1, 2],
    "author": 1,
    "status": "in_progress",
    "priority": "H",
    "due_date": "2026-02-15T17:00:00Z",
    "created_at": "2026-01-22T09:00:00Z",
    "updated_at": "2026-02-05T14:20:00Z"
  },
  {
    "id": 2,
    "name": "Implement authentication",
    "description": "Setup JWT authentication system",
    "project": 1,
    "assignees": [3],
    "author": 1,
    "status": "todo",
    "priority": "M",
    "due_date": "2026-02-20T17:00:00Z",
    "created_at": "2026-01-23T10:00:00Z",
    "updated_at": "2026-01-23T10:00:00Z"
  }
]
```

---

### 2. Create Task
**POST** `/tasks/create/`

Create a new task. The authenticated user becomes the task author.

**Permission:** Authenticated

**Request Body:**
```json
{
  "name": "string",
  "project": 1,
  "description": "string (optional)",
  "status": "todo | in_progress | done (optional, default: todo)",
  "priority": "L | M | H (optional, default: M)",
  "due_date": "2026-12-31T23:59:59Z (optional)",
  "assignee_ids": [1, 2, 3] (optional, array of user IDs)
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "New Task",
  "description": "Task description",
  "project": 1,
  "assignees": [1, 2],
  "author": 1,
  "status": "todo",
  "priority": "M",
  "due_date": "2026-02-28T17:00:00Z",
  "created_at": "2026-02-09T12:00:00Z",
  "updated_at": "2026-02-09T12:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "name": ["This field is required."],
  "project": ["This field is required."]
}
```

---

### 3. Get Task Details
**GET** `/tasks/<task_id>/`

Retrieve details of a specific task.

**Permission:** Authenticated

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Design homepage",
  "description": "Create mockups for the new homepage",
  "project": 1,
  "assignees": [1, 2],
  "author": 1,
  "status": "in_progress",
  "priority": "H",
  "due_date": "2026-02-15T17:00:00Z",
  "created_at": "2026-01-22T09:00:00Z",
  "updated_at": "2026-02-05T14:20:00Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Task not found"
}
```

---

### 4. Update Task
**PUT** `/tasks/<task_id>/update/`

Update task information.

**Permission:** Authenticated

**Request Body:**
```json
{
  "name": "string",
  "description": "string (optional)",
  "status": "todo | in_progress | done (optional)",
  "priority": "L | M | H (optional)",
  "due_date": "2026-12-31T23:59:59Z (optional)",
  "assignee_ids": [1, 2, 3] (optional, array of user IDs)
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Updated Task Name",
  "description": "Updated description",
  "project": 1,
  "assignees": [1, 3],
  "author": 1,
  "status": "done",
  "priority": "H",
  "due_date": "2026-02-15T17:00:00Z",
  "created_at": "2026-01-22T09:00:00Z",
  "updated_at": "2026-02-09T12:30:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Error message details"
}
```

---

### 5. Delete Task
**DELETE** `/tasks/<task_id>/delete/`

Delete a task.

**Permission:** Authenticated

**Response (204 No Content):**
```
No content returned
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Failed to delete task."
}
```

---

## Data Models

### User
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "avatar": "string (URL)",
  "date_joined": "datetime"
}
```

### Workspace
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "created_at": "datetime"
}
```

### Project
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "workspace": "integer (workspace_id)",
  "deadline": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Task
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "project": "integer (project_id)",
  "assignees": "array of integers (user_ids)",
  "author": "integer (user_id)",
  "status": "string (todo | in_progress | done)",
  "priority": "string (L | M | H)",
  "due_date": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Request successful with no content to return |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

---

## Error Response Format

All error responses follow this format:
```json
{
  "error": "Error message description"
}
```

Or for validation errors:
```json
{
  "field_name": ["Error message for this field"],
  "another_field": ["Another error message"]
}
```

---

## Notes

1. **Authentication**: All endpoints except `/auth/register/`, `/auth/token/`, and `/auth/token/refresh/` require JWT authentication.

2. **DateTime Format**: All datetime fields use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

3. **File Uploads**: The `avatar` field in user registration and update accepts multipart/form-data with image files.

4. **Task Status Values**:
   - `todo` - To Do
   - `in_progress` - In Progress
   - `done` - Done

5. **Task Priority Values**:
   - `L` - Low
   - `M` - Medium
   - `H` - High

6. **Filtering**: Some endpoints support query parameters for filtering results (e.g., tasks by project or user).

7. **Cascading Deletes**: 
   - Deleting a workspace will delete all its projects and associated tasks
   - Deleting a project will delete all its tasks
   - Task author can be set to NULL if the user is deleted

---

## Example Usage

### Register and Login Flow

1. **Register a new user:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secure123"}'
```

2. **Obtain access token:**
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secure123"}'
```

3. **Use the access token:**
```bash
curl -X GET http://localhost:8000/api/workspaces/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Create a Complete Workflow

1. **Create a workspace:**
```bash
curl -X POST http://localhost:8000/api/workspaces/create/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Workspace", "description": "Team workspace"}'
```

2. **Create a project in the workspace:**
```bash
curl -X POST http://localhost:8000/api/projects/create/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "workspace": 1, "deadline": "2026-12-31T23:59:59Z"}'
```

3. **Create a task in the project:**
```bash
curl -X POST http://localhost:8000/api/tasks/create/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Task", "project": 1, "priority": "H", "assignee_ids": [1]}'
```

---

## Support

For issues or questions, please contact the development team or refer to the project repository.
