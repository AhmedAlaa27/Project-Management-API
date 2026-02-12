"""
Unit tests for Workspaces app serializers.
"""

import pytest
from Workspaces.serializers import (
    WorkspaceSerializer,
    WorkspaceDetailSerializer,
    UpdateWorkspaceSerializer,
)

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestWorkspaceSerializer:
    """Test cases for WorkspaceSerializer."""

    def test_serializer_with_valid_data(self):
        """Test serializer with valid workspace data."""
        data = {
            "name": "Test Workspace",
            "description": "Test Description",
        }
        serializer = WorkspaceSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data["name"] == "Test Workspace"

    def test_serializer_output(self, workspace_factory):
        """Test serializer output contains correct fields."""
        workspace = workspace_factory(
            name="Test Workspace", description="Test Description"
        )
        serializer = WorkspaceSerializer(workspace)

        assert "id" in serializer.data
        assert serializer.data["name"] == "Test Workspace"
        assert serializer.data["description"] == "Test Description"
        assert "created_at" in serializer.data


@pytest.mark.unit
class TestWorkspaceDetailSerializer:
    """Test cases for WorkspaceDetailSerializer."""

    def test_nested_projects_serialization(self, workspace_factory, project_factory):
        """Test that projects are nested in the serializer output."""
        workspace = workspace_factory()
        project_factory(workspace=workspace, name="Project 1")
        project_factory(workspace=workspace, name="Project 2")

        serializer = WorkspaceDetailSerializer(workspace)

        assert "projects" in serializer.data
        assert len(serializer.data["projects"]) == 2

    def test_projects_are_read_only(self, workspace_factory):
        """Test that projects field is read-only."""
        workspace = workspace_factory()
        data = {
            "name": "Updated Workspace",
            "projects": [{"name": "New Project"}],  # Should be ignored
        }
        serializer = WorkspaceDetailSerializer(workspace, data=data, partial=True)

        # Should be valid even with projects in data (they're ignored)
        assert serializer.is_valid()


@pytest.mark.unit
class TestUpdateWorkspaceSerializer:
    """Test cases for UpdateWorkspaceSerializer."""

    def test_update_workspace_fields(self, workspace_factory):
        """Test updating workspace name and description."""
        workspace = workspace_factory(name="Old Name", description="Old Description")
        data = {
            "name": "New Name",
            "description": "New Description",
        }
        serializer = UpdateWorkspaceSerializer(workspace, data=data)

        assert serializer.is_valid()
        updated = serializer.save()
        assert updated.name == "New Name"
        assert updated.description == "New Description"

    def test_partial_update(self, workspace_factory):
        """Test partial update of workspace."""
        workspace = workspace_factory(
            name="Original", description="Original Description"
        )
        data = {"name": "Updated Name"}
        serializer = UpdateWorkspaceSerializer(workspace, data=data, partial=True)

        assert serializer.is_valid()
        updated = serializer.save()
        assert updated.name == "Updated Name"
        assert updated.description == "Original Description"
