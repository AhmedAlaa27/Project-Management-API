"""
Unit tests for Projects app serializers.
"""

import pytest
from django.utils import timezone
from datetime import timedelta
from Projects.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    CreateProjectSerializer,
    UpdateProjectSerializer,
)

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestProjectSerializer:
    """Test cases for ProjectSerializer."""

    def test_serializer_output(self, project_factory):
        """Test serializer output contains all fields."""
        project = project_factory(name="Test Project", description="Test Description")
        serializer = ProjectSerializer(project)

        assert "id" in serializer.data
        assert serializer.data["name"] == "Test Project"
        assert serializer.data["description"] == "Test Description"
        assert "workspace" in serializer.data
        assert "deadline" in serializer.data
        assert "created_at" in serializer.data
        assert "updated_at" in serializer.data


@pytest.mark.unit
class TestProjectDetailSerializer:
    """Test cases for ProjectDetailSerializer."""

    def test_nested_tasks_serialization(self, project_factory, task_factory):
        """Test that tasks are nested in serializer output."""
        project = project_factory()
        task_factory(project=project, name="Task 1")
        task_factory(project=project, name="Task 2")

        serializer = ProjectDetailSerializer(project)

        assert "tasks" in serializer.data
        assert len(serializer.data["tasks"]) == 2

    def test_tasks_are_read_only(self, project_factory):
        """Test that tasks field is read-only."""
        project = project_factory()
        data = {
            "name": "Updated Project",
            "tasks": [{"name": "New Task"}],  # Should be ignored
        }
        serializer = ProjectDetailSerializer(project, data=data, partial=True)

        assert serializer.is_valid()


@pytest.mark.unit
class TestCreateProjectSerializer:
    """Test cases for CreateProjectSerializer."""

    def test_create_project_with_all_fields(self, workspace_factory):
        """Test creating project with all fields."""
        workspace = workspace_factory()
        deadline = timezone.now() + timedelta(days=30)
        data = {
            "name": "New Project",
            "description": "New Description",
            "workspace": workspace.id,
            "deadline": deadline.isoformat(),
        }
        serializer = CreateProjectSerializer(data=data)

        assert serializer.is_valid()
        project = serializer.save()
        assert project.name == "New Project"
        assert project.workspace == workspace

    def test_create_project_minimal_fields(self, workspace_factory):
        """Test creating project with minimal required fields."""
        workspace = workspace_factory()
        data = {
            "name": "New Project",
            "workspace": workspace.id,
        }
        serializer = CreateProjectSerializer(data=data)

        assert serializer.is_valid()

    def test_missing_required_fields(self):
        """Test validation fails with missing required fields."""
        data = {"description": "Only description"}
        serializer = CreateProjectSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors
        assert "workspace" in serializer.errors


@pytest.mark.unit
class TestUpdateProjectSerializer:
    """Test cases for UpdateProjectSerializer."""

    def test_update_project_fields(self, project_factory):
        """Test updating project fields."""
        project = project_factory(name="Old Name", description="Old Description")
        deadline = timezone.now() + timedelta(days=60)
        data = {
            "name": "New Name",
            "description": "New Description",
            "deadline": deadline.isoformat(),
        }
        serializer = UpdateProjectSerializer(project, data=data)

        assert serializer.is_valid()
        updated = serializer.save()
        assert updated.name == "New Name"
        assert updated.description == "New Description"

    def test_partial_update(self, project_factory):
        """Test partial update of project."""
        project = project_factory(name="Original", description="Original Description")
        data = {"name": "Updated Name"}
        serializer = UpdateProjectSerializer(project, data=data, partial=True)

        assert serializer.is_valid()
        updated = serializer.save()
        assert updated.name == "Updated Name"
        assert updated.description == "Original Description"
