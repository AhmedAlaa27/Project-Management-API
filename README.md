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
- **MySQL** - Database
- **pytest** - Testing framework
- **Factory Boy** - Test data generation
- **python-dotenv** - Environment configuration

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

4. **Set up environment variables**
Create a `.env` file in the project root with your database credentials:
```
DB_NAME=your_database_name
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
SECRET_KEY=your_secret_key
DEBUG=True
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
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
├── utils/               # Utility functions (standardized responses)
├── tests/               # Integration tests and test factories
├── media/               # Media files (avatars)
├── conftest.py          # Pytest configuration and fixtures
├── pytest.ini           # Pytest settings
└── manage.py
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

## Testing

The project uses **pytest** with comprehensive test coverage:

### Run all tests
```bash
pytest
```

### Run specific test categories
```bash
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests
```

### Run tests for a specific app
```bash
pytest Users/           # Test Users app
pytest Projects/        # Test Projects app
```

### Run with coverage
```bash
pytest --cov=Users --cov=Workspaces --cov=Projects --cov=Tasks
```

### Test Structure
- **Unit Tests**: Test models, serializers, and services
- **Integration Tests**: Test API endpoints and workflows
- **Test Factories**: Generate realistic test data using Factory Boy
- **Fixtures**: Shared test utilities in `conftest.py`

## Development

### Access Django admin
Navigate to `http://localhost:8000/admin/` and login with superuser credentials.

### Standardized API Responses
All endpoints return consistent response format using utility functions:
```json
{
  "success": true/false,
  "message": "Response message",
  "data": {...},
  "errors": null
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact

For questions or support, please open an issue in the repository.
