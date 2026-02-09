# Project Management API

A RESTful API built with Django and Django REST Framework for managing projects, tasks, workspaces, and team collaboration.

## Features

- 🔐 **JWT Authentication** - Secure user authentication with access and refresh tokens
- 👥 **User Management** - User registration, profiles, and avatar uploads
- 🏢 **Workspaces** - Create and manage team workspaces
- 📁 **Projects** - Organize work into projects within workspaces
- ✅ **Tasks** - Create, assign, and track tasks with priorities and statuses

## Tech Stack

- **Python 3.x**
- **Django 6.0**
- **Django REST Framework**
- **Simple JWT** - JWT authentication
- **MySQL** - Database (development)

## Installation

1. **Clone the repository**
```bash
git clone git@github.com:AhmedAlaa27/Project-Management-API.git
cd Project-Management-API
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Quick Start

1. **Register a new user**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secure123"}'
```

2. **Get access token**
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secure123"}'
```

3. **Create a workspace**
```bash
curl -X POST http://localhost:8000/api/workspaces/create/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Workspace"}'
```

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/register/` - Register new user

### Users
- `GET /api/auth/` - List all users
- `GET /api/auth/<user_id>/` - Get user details
- `PUT /api/auth/<user_id>/update/` - Update user
- `DELETE /api/auth/<user_id>/delete/` - Delete user

### Workspaces
- `GET /api/workspaces/` - List all workspaces
- `GET /api/workspaces/me/` - List user's workspaces
- `POST /api/workspaces/create/` - Create workspace
- `GET /api/workspaces/<id>/` - Get workspace details
- `PUT /api/workspaces/<id>/update/` - Update workspace
- `DELETE /api/workspaces/<id>/delete/` - Delete workspace

### Projects
- `GET /api/projects/` - List projects (filterable by workspace)
- `POST /api/projects/create/` - Create project
- `GET /api/projects/<id>/` - Get project details
- `PUT /api/projects/<id>/update/` - Update project
- `DELETE /api/projects/<id>/delete/` - Delete project

### Tasks
- `GET /api/tasks/` - List tasks (filterable by project/user)
- `POST /api/tasks/create/` - Create task
- `GET /api/tasks/<id>/` - Get task details
- `PUT /api/tasks/<id>/update/` - Update task
- `DELETE /api/tasks/<id>/delete/` - Delete task

📖 **For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)**

## Project Structure

```
Project-Management-API/
├── pmtool/              # Main project settings
├── Users/               # User management app
├── Workspaces/          # Workspace management app
├── Projects/            # Project management app
├── Tasks/               # Task management app
├── media/               # Media files (avatars)
├── manage.py
└── db.sqlite3
```

## Key Features Explained

### Task Management
- **Status Options**: `todo`, `in_progress`, `done`
- **Priority Levels**: `L` (Low), `M` (Medium), `H` (High)
- **Multiple Assignees**: Tasks can be assigned to multiple users
- **Author Tracking**: Each task records who created it

### Workspaces
- Every workspace has an owner and can have multiple members
- Projects are organized within workspaces
- Deleting a workspace cascades to delete projects and tasks

### Authentication
- Uses JWT tokens with access and refresh token system
- Access tokens expire and can be refreshed using refresh tokens
- Protected endpoints require Bearer token in Authorization header

## Development

### Run tests
```bash
python manage.py test
```

### Access Django admin
Navigate to `http://localhost:8000/admin/` and login with superuser credentials.

### Media files
User avatars are stored in `media/avatars/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

For questions or support, please open an issue in the repository.
