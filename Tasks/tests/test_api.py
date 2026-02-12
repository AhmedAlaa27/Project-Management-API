"""
Integration tests for Tasks app API endpoints.
"""

import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from Tasks.models import Task

pytestmark = pytest.mark.django_db


@pytest.mark.integration
class TestCreateTaskAPI:
    """Test cases for task creation endpoint."""

    def test_create_task_authenticated(
        self, authenticated_client, authenticated_user, project_factory
    ):
        """Test creating task with authentication."""
        project = project_factory()
        url = reverse("create_task")
        due_date = timezone.now() + timedelta(days=7)
        data = {
            "name": "New Task",
            "description": "New Description",
            "project": project.id,
            "status": Task.Status.TODO,
            "priority": Task.Priority.HIGH,
            "due_date": due_date.isoformat(),
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["data"]["name"] == "New Task"
        # Verify task author is set to request.user
        task = Task.objects.get(id=response.data["data"]["id"])
        assert task.author == authenticated_user

    def test_create_task_with_assignees(
        self, authenticated_client, project_factory, user_factory
    ):
        """Test creating task with assignees."""
        project = project_factory()
        user1 = user_factory()
        user2 = user_factory()
        url = reverse("create_task")
        data = {
            "name": "New Task",
            "project": project.id,
            "assignee_ids": [user1.id, user2.id],
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        task = Task.objects.get(id=response.data["data"]["id"])
        assert task.assignees.count() == 2

    def test_create_task_without_assignees(self, authenticated_client, project_factory):
        """Test creating task without assignees."""
        project = project_factory()
        url = reverse("create_task")
        data = {
            "name": "New Task",
            "project": project.id,
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_task_invalid_status(self, authenticated_client, project_factory):
        """Test creating task with invalid status."""
        project = project_factory()
        url = reverse("create_task")
        data = {
            "name": "New Task",
            "project": project.id,
            "status": "invalid_status",
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_task_invalid_priority(self, authenticated_client, project_factory):
        """Test creating task with invalid priority."""
        project = project_factory()
        url = reverse("create_task")
        data = {
            "name": "New Task",
            "project": project.id,
            "priority": "invalid_priority",
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_task_invalid_project(self, authenticated_client):
        """Test creating task with invalid project ID."""
        url = reverse("create_task")
        data = {
            "name": "New Task",
            "project": 9999,
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_task_unauthenticated(self, api_client, project_factory):
        """Test creating task fails without authentication."""
        project = project_factory()
        url = reverse("create_task")
        data = {
            "name": "New Task",
            "project": project.id,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestListTasksAPI:
    """Test cases for listing tasks."""

    def test_list_all_tasks(self, authenticated_client, task_factory):
        """Test listing all tasks."""
        task_factory.create_batch(3)
        url = reverse("task_list")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]) >= 3

    def test_list_tasks_filtered_by_project(
        self, authenticated_client, project_factory, task_factory
    ):
        """Test filtering tasks by project."""
        project = project_factory()
        task_factory(project=project)
        task_factory(project=project)
        task_factory()  # Different project
        url = f"{reverse('task_list')}?project_id={project.id}"

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2

    def test_list_tasks_filtered_by_user(
        self, authenticated_client, authenticated_user, task_factory
    ):
        """Test filtering tasks by assigned user (uses request.user)."""
        task_factory(assignees=[authenticated_user])
        task_factory(assignees=[authenticated_user])
        task_factory()  # Not assigned to authenticated user
        url = f"{reverse('task_list')}?user_id={authenticated_user.id}"

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2

    def test_list_tasks_unauthenticated(self, api_client):
        """Test listing tasks fails without authentication."""
        url = reverse("task_list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestTaskDetailAPI:
    """Test cases for task detail endpoint."""

    def test_get_task_detail(self, authenticated_client, task_factory):
        """Test getting task details."""
        task = task_factory(name="Test Task")
        url = reverse("task_detail", kwargs={"task_id": task.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["name"] == "Test Task"

    def test_get_task_detail_unauthenticated(self, api_client, task_factory):
        """Test getting task detail fails without authentication."""
        task = task_factory()
        url = reverse("task_detail", kwargs={"task_id": task.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_nonexistent_task(self, authenticated_client):
        """Test getting nonexistent task."""
        url = reverse("task_detail", kwargs={"task_id": 9999})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
class TestUpdateTaskAPI:
    """Test cases for updating task."""

    def test_update_task_authenticated(self, authenticated_client, task_factory):
        """Test updating task with authentication."""
        task = task_factory(
            name="Old Name",
            description="Old Desc",
            status=Task.Status.TODO,
            priority=Task.Priority.LOW,
        )
        url = reverse("update_task", kwargs={"task_id": task.id})
        due_date = timezone.now() + timedelta(days=14)
        data = {
            "name": "New Name",
            "description": "New Description",
            "status": Task.Status.DONE,
            "priority": Task.Priority.HIGH,
            "due_date": due_date.isoformat(),
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["name"] == "New Name"
        assert response.data["data"]["status"] == "done"
        assert response.data["data"]["priority"] == "H"

    def test_update_task_assignees(
        self, authenticated_client, task_factory, user_factory
    ):
        """Test updating task assignees."""
        task = task_factory()
        user1 = user_factory()
        user2 = user_factory()
        url = reverse("update_task", kwargs={"task_id": task.id})
        data = {
            "name": task.name,
            "assignee_ids": [user1.id, user2.id],
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.assignees.count() == 2

    def test_update_task_status(self, authenticated_client, task_factory):
        """Test updating task status."""
        task = task_factory(status=Task.Status.TODO)
        url = reverse("update_task", kwargs={"task_id": task.id})
        data = {
            "name": task.name,
            "status": Task.Status.DONE,
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["status"] == "done"

    def test_update_task_priority(self, authenticated_client, task_factory):
        """Test updating task priority."""
        task = task_factory(priority=Task.Priority.LOW)
        url = reverse("update_task", kwargs={"task_id": task.id})
        data = {
            "name": task.name,
            "priority": Task.Priority.HIGH,
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["priority"] == "H"

    def test_update_task_partial(self, authenticated_client, task_factory):
        """Test partial update of task."""
        task = task_factory(name="Original", status=Task.Status.TODO)
        url = reverse("update_task", kwargs={"task_id": task.id})
        data = {"name": "Updated Name"}

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["name"] == "Updated Name"

    def test_update_task_unauthenticated(self, api_client, task_factory):
        """Test updating task fails without authentication."""
        task = task_factory()
        url = reverse("update_task", kwargs={"task_id": task.id})
        data = {"name": "New Name"}

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestDeleteTaskAPI:
    """Test cases for deleting task."""

    def test_delete_task_authenticated(self, authenticated_client, task_factory):
        """Test deleting task with authentication."""
        task = task_factory()
        url = reverse("delete_task", kwargs={"task_id": task.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert not Task.objects.filter(id=task.id).exists()

    def test_delete_task_unauthenticated(self, api_client, task_factory):
        """Test deleting task fails without authentication."""
        task = task_factory()
        url = reverse("delete_task", kwargs={"task_id": task.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_nonexistent_task(self, authenticated_client):
        """Test deleting nonexistent task."""
        url = reverse("delete_task", kwargs={"task_id": 9999})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
class TestTaskAuthorBehavior:
    """Test cases for task author-related behavior."""

    def test_author_deletion_sets_null(
        self, authenticated_client, task_factory, user_factory
    ):
        """Test that deleting author sets task.author to NULL."""
        author = user_factory()
        task = task_factory(author=author)
        author_id = author.id

        # Delete the author
        author.delete()
        task.refresh_from_db()

        # Task should still exist but author should be NULL
        assert Task.objects.filter(id=task.id).exists()
        assert task.author is None
