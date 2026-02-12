"""
Unit tests for Tasks app models.
"""

import pytest
from django.contrib.auth import get_user_model
from Tasks.models import Task

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestTaskModel:
    """Test cases for the Task model."""

    def test_task_creation_with_all_fields(self, task_factory):
        """Test creating a task with all fields."""
        task = task_factory(
            name="Test Task",
            description="Test Description",
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.HIGH,
        )

        assert task.name == "Test Task"
        assert task.description == "Test Description"
        assert task.status == Task.Status.IN_PROGRESS
        assert task.priority == Task.Priority.HIGH
        assert task.project is not None

    def test_str_method_with_author(self, task_factory):
        """Test string representation with author."""
        task = task_factory(
            name="My Task",
            project__name="My Project",
            project__workspace__name="My Workspace",
            author__username="testuser",
        )

        result = str(task)

        assert result == "My Task | My Project | My Workspace | testuser"

    def test_str_method_without_author(self, task_factory, user_factory):
        """Test string representation when author is None."""
        task = task_factory(
            name="My Task",
            project__name="My Project",
            project__workspace__name="My Workspace",
            author=None,
        )

        result = str(task)

        assert result == "My Task | My Project | My Workspace | No Author"

    def test_project_relationship(self, task_factory, project_factory):
        """Test task-project foreign key relationship."""
        project = project_factory(name="Test Project")
        task = task_factory(project=project)

        assert task.project.id == project.id
        assert task.project.name == "Test Project"

    def test_author_relationship(self, task_factory, user_factory):
        """Test task-author foreign key relationship."""
        author = user_factory(username="taskauthor")
        task = task_factory(author=author)

        assert task.author.id == author.id
        assert task.author.username == "taskauthor"

    def test_assignees_many_to_many(self, task_factory, user_factory):
        """Test task assignees many-to-many relationship."""
        user1 = user_factory(username="user1")
        user2 = user_factory(username="user2")
        task = task_factory(assignees=[user1, user2])

        assert task.assignees.count() == 2
        assert user1 in task.assignees.all()
        assert user2 in task.assignees.all()

    def test_status_choices(self, task_factory):
        """Test status field choices."""
        task_todo = task_factory(status=Task.Status.TODO)
        task_in_progress = task_factory(status=Task.Status.IN_PROGRESS)
        task_done = task_factory(status=Task.Status.DONE)

        assert task_todo.status == "todo"
        assert task_in_progress.status == "in_progress"
        assert task_done.status == "done"

    def test_priority_choices(self, task_factory):
        """Test priority field choices."""
        task_low = task_factory(priority=Task.Priority.LOW)
        task_medium = task_factory(priority=Task.Priority.MEDIUM)
        task_high = task_factory(priority=Task.Priority.HIGH)

        assert task_low.priority == "L"
        assert task_medium.priority == "M"
        assert task_high.priority == "H"

    def test_default_status_is_todo(self, task_factory):
        """Test that default status is TODO."""
        task = task_factory()

        assert task.status == Task.Status.TODO

    def test_default_priority_is_medium(self, task_factory):
        """Test that default priority is MEDIUM."""
        task = task_factory()

        assert task.priority == Task.Priority.MEDIUM

    def test_author_can_be_null(self, task_factory):
        """Test that author field can be null."""
        task = task_factory(author=None)

        assert task.author is None

    def test_due_date_optional(self, task_factory):
        """Test that due_date field is optional."""
        task = task_factory(due_date=None)

        assert task.due_date is None

    def test_description_optional(self, task_factory):
        """Test that description field is optional."""
        task = task_factory(description=None)

        assert task.description is None

    def test_author_deletion_sets_null(self, task_factory, user_factory):
        """Test that deleting author sets field to NULL."""
        author = user_factory()
        task = task_factory(author=author)
        author_id = author.id

        author.delete()
        task.refresh_from_db()

        assert task.author is None

    def test_created_at_auto_timestamp(self, task_factory):
        """Test that created_at is automatically set."""
        task = task_factory()

        assert task.created_at is not None

    def test_updated_at_auto_timestamp(self, task_factory):
        """Test that updated_at is automatically set."""
        task = task_factory()

        assert task.updated_at is not None
