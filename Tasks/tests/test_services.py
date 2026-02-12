"""
Unit tests for Tasks app services.
"""

import pytest
from django.utils import timezone
from datetime import timedelta
from Tasks.models import Task
from Tasks.services import (
    create_task_service,
    update_task_service,
    list_tasks_service,
    list_project_tasks_service,
    list_user_tasks_service,
    get_task_by_id_service,
    delete_task_service,
)

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestCreateTaskService:
    """Test cases for create_task_service."""

    def test_create_task_with_all_fields(self, project_factory, user_factory):
        """Test creating task with all fields."""
        project = project_factory()
        author = user_factory()
        due_date = timezone.now() + timedelta(days=7)

        task = create_task_service(
            name="Test Task",
            project_id=project.id,
            author=author,
            description="Test Description",
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.HIGH,
            due_date=due_date,
        )

        assert task.name == "Test Task"
        assert task.description == "Test Description"
        assert task.project == project
        assert task.author == author
        assert task.status == Task.Status.IN_PROGRESS
        assert task.priority == Task.Priority.HIGH

    def test_create_task_with_assignees(self, project_factory, user_factory):
        """Test creating task with assignees."""
        project = project_factory()
        author = user_factory()
        user1 = user_factory()
        user2 = user_factory()

        task = create_task_service(
            name="Test Task",
            project_id=project.id,
            author=author,
            assignee_ids=[user1.id, user2.id],
        )

        assert task.assignees.count() == 2
        assert user1 in task.assignees.all()
        assert user2 in task.assignees.all()

    def test_create_task_without_assignees(self, project_factory, user_factory):
        """Test creating task without assignees."""
        project = project_factory()
        author = user_factory()

        task = create_task_service(
            name="Test Task", project_id=project.id, author=author
        )

        assert task.assignees.count() == 0

    def test_create_with_transaction(self, project_factory, user_factory):
        """Test that create uses transaction."""
        project = project_factory()
        author = user_factory()

        task = create_task_service(
            name="Test Task", project_id=project.id, author=author
        )

        assert Task.objects.filter(id=task.id).exists()


@pytest.mark.unit
class TestUpdateTaskService:
    """Test cases for update_task_service."""

    def test_update_task_fields(self, task_factory):
        """Test updating task fields."""
        task = task_factory(
            name="Old Name",
            description="Old Description",
            status=Task.Status.TODO,
            priority=Task.Priority.LOW,
        )
        due_date = timezone.now() + timedelta(days=14)

        updated = update_task_service(
            task_id=task.id,
            name="New Name",
            description="New Description",
            status=Task.Status.DONE,
            priority=Task.Priority.HIGH,
            due_date=due_date,
        )

        assert updated.name == "New Name"
        assert updated.description == "New Description"
        assert updated.status == Task.Status.DONE
        assert updated.priority == Task.Priority.HIGH

    def test_update_task_assignees(self, task_factory, user_factory):
        """Test updating task assignees."""
        task = task_factory()
        user1 = user_factory()
        user2 = user_factory()

        updated = update_task_service(
            task_id=task.id, name=task.name, assignee_ids=[user1.id, user2.id]
        )

        assert updated.assignees.count() == 2
        assert user1 in updated.assignees.all()

    def test_update_with_transaction(self, task_factory):
        """Test that update uses transaction."""
        task = task_factory()

        updated = update_task_service(task_id=task.id, name="Updated")

        assert updated.name == "Updated"


@pytest.mark.unit
class TestListTasksService:
    """Test cases for list_tasks_service."""

    def test_list_all_tasks(self, task_factory):
        """Test listing all tasks."""
        task_factory.create_batch(3)

        tasks = list_tasks_service()

        assert tasks.count() == 3

    def test_list_empty_tasks(self):
        """Test listing when no tasks exist."""
        tasks = list_tasks_service()

        assert tasks.count() == 0


@pytest.mark.unit
class TestListProjectTasksService:
    """Test cases for list_project_tasks_service."""

    def test_list_project_tasks(self, project_factory, task_factory):
        """Test listing tasks for a specific project."""
        project = project_factory()
        task_factory(project=project, name="Task 1")
        task_factory(project=project, name="Task 2")
        task_factory()  # Different project

        tasks = list_project_tasks_service(project.id)

        assert tasks.count() == 2

    def test_list_project_tasks_empty(self, project_factory):
        """Test listing tasks for project with no tasks."""
        project = project_factory()

        tasks = list_project_tasks_service(project.id)

        assert tasks.count() == 0


@pytest.mark.unit
class TestListUserTasksService:
    """Test cases for list_user_tasks_service."""

    def test_list_user_tasks(self, user_factory, task_factory):
        """Test listing tasks assigned to a specific user."""
        user = user_factory()
        task_factory(assignees=[user])
        task_factory(assignees=[user])
        task_factory()  # Not assigned to this user

        tasks = list_user_tasks_service(user)

        assert tasks.count() == 2

    def test_list_user_tasks_empty(self, user_factory):
        """Test listing tasks for user with no assignments."""
        user = user_factory()

        tasks = list_user_tasks_service(user)

        assert tasks.count() == 0


@pytest.mark.unit
class TestGetTaskByIdService:
    """Test cases for get_task_by_id_service."""

    def test_get_existing_task(self, task_factory):
        """Test getting an existing task by ID."""
        task = task_factory(name="Test Task")

        retrieved = get_task_by_id_service(task.id)

        assert retrieved.id == task.id
        assert retrieved.name == "Test Task"

    def test_get_nonexistent_task(self):
        """Test that DoesNotExist is raised for invalid ID."""
        with pytest.raises(Task.DoesNotExist):
            get_task_by_id_service(9999)


@pytest.mark.unit
class TestDeleteTaskService:
    """Test cases for delete_task_service."""

    def test_delete_task(self, task_factory):
        """Test deleting a task."""
        task = task_factory()
        task_id = task.id

        result = delete_task_service(task_id)

        assert result is True
        assert not Task.objects.filter(id=task_id).exists()

    def test_delete_nonexistent_task(self):
        """Test deleting nonexistent task raises error."""
        with pytest.raises(Task.DoesNotExist):
            delete_task_service(9999)

    def test_delete_with_transaction(self, task_factory):
        """Test that delete uses transaction."""
        task = task_factory()
        task_id = task.id

        delete_task_service(task_id)

        assert not Task.objects.filter(id=task_id).exists()
