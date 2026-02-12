"""
Unit tests for Workspaces app models.
"""

import pytest
from Workspaces.models import Workspace

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestWorkspaceModel:
    """Test cases for the Workspace model."""

    def test_workspace_creation_with_all_fields(self, workspace_factory):
        """Test creating a workspace with all fields."""
        workspace = workspace_factory(
            name="Test Workspace", description="Test Description"
        )

        assert workspace.name == "Test Workspace"
        assert workspace.description == "Test Description"
        assert workspace.owner is not None
        assert workspace.id is not None

    def test_str_method(self, workspace_factory):
        """Test string representation of workspace."""
        workspace = workspace_factory(name="Test Workspace", owner__username="testuser")

        result = str(workspace)

        assert result == "Test Workspace | testuser"

    def test_owner_relationship(self, workspace_factory, user_factory):
        """Test workspace-owner foreign key relationship."""
        owner = user_factory(username="workspaceowner")
        workspace = workspace_factory(owner=owner)

        assert workspace.owner.id == owner.id
        assert workspace.owner.username == "workspaceowner"

    def test_members_relationship(self, workspace_factory, user_factory):
        """Test workspace members many-to-many relationship."""
        user1 = user_factory(username="user1")
        user2 = user_factory(username="user2")
        workspace = workspace_factory(members=[user1, user2])

        assert workspace.members.count() == 2
        assert user1 in workspace.members.all()
        assert user2 in workspace.members.all()

    def test_created_at_auto_timestamp(self, workspace_factory):
        """Test that created_at is automatically set."""
        workspace = workspace_factory()

        assert workspace.created_at is not None

    def test_updated_at_auto_timestamp(self, workspace_factory):
        """Test that updated_at is automatically set."""
        workspace = workspace_factory()

        assert workspace.updated_at is not None

    def test_description_optional(self, workspace_factory):
        """Test that description field is optional."""
        workspace = workspace_factory(description=None)

        assert workspace.description is None

    def test_reverse_relation_projects(self, workspace_factory, project_factory):
        """Test reverse relationship to projects."""
        workspace = workspace_factory()
        project_factory(workspace=workspace, name="Project 1")
        project_factory(workspace=workspace, name="Project 2")

        assert workspace.projects.count() == 2
