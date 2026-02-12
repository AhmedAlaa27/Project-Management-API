"""
Unit tests for Tasks app serializers.
"""

import pytest
from django.utils import timezone
from datetime import timedelta
from Tasks.models import Task
from Tasks.serializers import (
    TaskSerializer,
    CreateTaskSerializer,
    UpdateTaskSerializer,
)

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestTaskSerializer:
    """Test cases for TaskSerializer."""

    def test_serializer_output(self, task_factory):
        """Test serializer output contains all fields."""
        task = task_factory(
            name="Test Task",
            description="Test Description",
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.HIGH,
        )
        serializer = TaskSerializer(task)

        assert "id" in serializer.data
        assert serializer.data["name"] == "Test Task"
        assert serializer.data["description"] == "Test Description"
        assert serializer.data["status"] == "in_progress"
        assert serializer.data["priority"] == "H"
        assert "project" in serializer.data
        assert "assignees" in serializer.data
        assert "author" in serializer.data
        assert "due_date" in serializer.data


@pytest.mark.unit
class TestCreateTaskSerializer:
    """Test cases for CreateTaskSerializer."""

    def test_create_task_with_all_fields(self, project_factory, user_factory):
        """Test creating task with all fields."""
        project = project_factory()
        due_date = timezone.now() + timedelta(days=7)
        data = {
            "name": "New Task",
            "description": "Task Description",
            "project": project.id,
            "status": Task.Status.TODO,
            "priority": Task.Priority.HIGH,
            "due_date": due_date.isoformat(),
            "assignee_ids": [],
        }
        serializer = CreateTaskSerializer(data=data)

        assert serializer.is_valid()

    def test_create_task_with_assignees(self, project_factory, user_factory):
        """Test creating task with assignees."""
        project = project_factory()
        user1 = user_factory()
        user2 = user_factory()
        data = {
            "name": "New Task",
            "project": project.id,
            "assignee_ids": [user1.id, user2.id],
        }
        serializer = CreateTaskSerializer(data=data)

        assert serializer.is_valid()
        assert "assignee_ids" in serializer.validated_data

    def test_assignee_ids_is_write_only(self, project_factory):
        """Test that assignee_ids is write-only."""
        project = project_factory()
        data = {
            "name": "New Task",
            "project": project.id,
            "assignee_ids": [1, 2],
        }
        serializer = CreateTaskSerializer(data=data)
        serializer.is_valid()

        # assignee_ids should not appear in validated_data output
        # when serializing (it's write-only)

    def test_assignee_ids_optional(self, project_factory):
        """Test that assignee_ids is optional."""
        project = project_factory()
        data = {
            "name": "New Task",
            "project": project.id,
        }
        serializer = CreateTaskSerializer(data=data)

        assert serializer.is_valid()

    def test_missing_required_fields(self):
        """Test validation fails with missing required fields."""
        data = {"description": "Only description"}
        serializer = CreateTaskSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors
        assert "project" in serializer.errors

    def test_status_choices_validation(self, project_factory):
        """Test that invalid status choice is rejected."""
        project = project_factory()
        data = {
            "name": "New Task",
            "project": project.id,
            "status": "invalid_status",
        }
        serializer = CreateTaskSerializer(data=data)

        assert not serializer.is_valid()

    def test_priority_choices_validation(self, project_factory):
        """Test that invalid priority choice is rejected."""
        project = project_factory()
        data = {
            "name": "New Task",
            "project": project.id,
            "priority": "invalid_priority",
        }
        serializer = CreateTaskSerializer(data=data)

        assert not serializer.is_valid()


@pytest.mark.unit
class TestUpdateTaskSerializer:
    """Test cases for UpdateTaskSerializer."""

    def test_update_task_fields(self, task_factory):
        """Test updating task fields."""
        task = task_factory(
            name="Old Name",
            description="Old Description",
            status=Task.Status.TODO,
            priority=Task.Priority.LOW,
        )
        due_date = timezone.now() + timedelta(days=14)
        data = {
            "name": "New Name",
            "description": "New Description",
            "status": Task.Status.IN_PROGRESS,
            "priority": Task.Priority.HIGH,
            "due_date": due_date.isoformat(),
        }
        serializer = UpdateTaskSerializer(task, data=data)

        assert serializer.is_valid()
        updated = serializer.save()
        assert updated.name == "New Name"
        assert updated.status == Task.Status.IN_PROGRESS
        assert updated.priority == Task.Priority.HIGH

    def test_update_assignees(self, task_factory, user_factory):
        """Test updating task assignees."""
        task = task_factory()
        user1 = user_factory()
        user2 = user_factory()
        data = {
            "name": task.name,
            "assignee_ids": [user1.id, user2.id],
        }
        serializer = UpdateTaskSerializer(task, data=data, partial=True)

        assert serializer.is_valid()

    def test_partial_update(self, task_factory):
        """Test partial update of task."""
        task = task_factory(name="Original", status=Task.Status.TODO)
        data = {"status": Task.Status.DONE}
        serializer = UpdateTaskSerializer(task, data=data, partial=True)

        assert serializer.is_valid()
        updated = serializer.save()
        assert updated.status == Task.Status.DONE
        assert updated.name == "Original"
