"""
Unit tests for Projects app models.
"""

import pytest
from Projects.models import Project

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestProjectModel:
    """Test cases for the Project model."""

    def test_project_creation_with_all_fields(self, project_factory):
        """Test creating a project with all fields."""
        project = project_factory(name="Test Project", description="Test Description")

        assert project.name == "Test Project"
        assert project.description == "Test Description"
        assert project.workspace is not None
        assert project.id is not None

    def test_str_method(self, project_factory):
        """Test string representation of project."""
        project = project_factory(
            name="My Project",
            workspace__name="My Workspace",
            workspace__owner__username="testuser",
        )

        result = str(project)

        assert result == "My Project | My Workspace | testuser"

    def test_workspace_relationship(self, project_factory, workspace_factory):
        """Test project-workspace foreign key relationship."""
        workspace = workspace_factory(name="Test Workspace")
        project = project_factory(workspace=workspace)

        assert project.workspace.id == workspace.id
        assert project.workspace.name == "Test Workspace"

    def test_deadline_field_optional(self, project_factory):
        """Test that deadline field is optional."""
        project = project_factory(deadline=None)

        assert project.deadline is None

    def test_created_at_auto_timestamp(self, project_factory):
        """Test that created_at is automatically set."""
        project = project_factory()

        assert project.created_at is not None

    def test_updated_at_auto_timestamp(self, project_factory):
        """Test that updated_at is automatically set."""
        project = project_factory()

        assert project.updated_at is not None

    def test_description_optional(self, project_factory):
        """Test that description field is optional."""
        project = project_factory(description=None)

        assert project.description is None

    def test_reverse_relation_tasks(self, project_factory, task_factory):
        """Test reverse relationship to tasks."""
        project = project_factory()
        task_factory(project=project, name="Task 1")
        task_factory(project=project, name="Task 2")

        assert project.tasks.count() == 2
