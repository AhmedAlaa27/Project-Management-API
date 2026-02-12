"""
Unit tests for Workspaces app services.
"""

import pytest
from Workspaces.models import Workspace
from Workspaces.services import (
    create_workspace_service,
    update_workspace_service,
    list_workspaces_service,
    user_list_workspaces_service,
    get_workspace_by_id_service,
    delete_workspace_service,
)

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestCreateWorkspaceService:
    """Test cases for create_workspace_service."""

    def test_create_workspace_with_all_fields(self, user_factory):
        """Test creating workspace with all fields."""
        owner = user_factory(username="owner")

        workspace = create_workspace_service(
            name="Test Workspace", owner=owner, description="Test Description"
        )

        assert workspace.name == "Test Workspace"
        assert workspace.description == "Test Description"
        assert workspace.owner == owner

    def test_owner_automatically_added_to_members(self, user_factory):
        """Test that owner is automatically added to members."""
        owner = user_factory()

        workspace = create_workspace_service(name="Test Workspace", owner=owner)

        assert owner in workspace.members.all()
        assert workspace.members.count() == 1

    def test_create_with_transaction(self, user_factory):
        """Test that create uses transaction."""
        owner = user_factory()

        workspace = create_workspace_service(name="Test Workspace", owner=owner)

        # Should be committed successfully
        assert Workspace.objects.filter(id=workspace.id).exists()


@pytest.mark.unit
class TestUpdateWorkspaceService:
    """Test cases for update_workspace_service."""

    def test_update_workspace_fields(self, workspace_factory):
        """Test updating workspace name and description."""
        workspace = workspace_factory(name="Old Name", description="Old Description")

        updated = update_workspace_service(
            workspace_id=workspace.id, name="New Name", description="New Description"
        )

        assert updated.name == "New Name"
        assert updated.description == "New Description"

    def test_update_with_transaction(self, workspace_factory):
        """Test that update uses transaction."""
        workspace = workspace_factory()

        updated = update_workspace_service(workspace_id=workspace.id, name="Updated")

        assert updated.name == "Updated"


@pytest.mark.unit
class TestListWorkspacesService:
    """Test cases for list_workspaces_service."""

    def test_list_all_workspaces(self, workspace_factory):
        """Test listing all workspaces."""
        workspace_factory.create_batch(3)

        workspaces = list_workspaces_service()

        assert workspaces.count() == 3

    def test_list_empty_workspaces(self):
        """Test listing when no workspaces exist."""
        workspaces = list_workspaces_service()

        assert workspaces.count() == 0


@pytest.mark.unit
class TestUserListWorkspacesService:
    """Test cases for user_list_workspaces_service."""

    def test_list_user_workspaces(self, workspace_factory, user_factory):
        """Test listing workspaces for a specific user."""
        user = user_factory()
        workspace1 = workspace_factory(members=[user])
        workspace2 = workspace_factory(members=[user])
        workspace_factory()  # Another workspace without the user

        workspaces = user_list_workspaces_service(user)

        assert workspaces.count() == 2
        assert workspace1 in workspaces
        assert workspace2 in workspaces

    def test_list_user_workspaces_empty(self, user_factory):
        """Test listing workspaces for user with no memberships."""
        user = user_factory()

        workspaces = user_list_workspaces_service(user)

        assert workspaces.count() == 0


@pytest.mark.unit
class TestGetWorkspaceByIdService:
    """Test cases for get_workspace_by_id_service."""

    def test_get_existing_workspace(self, workspace_factory):
        """Test getting an existing workspace by ID."""
        workspace = workspace_factory(name="Test Workspace")

        retrieved = get_workspace_by_id_service(workspace.id)

        assert retrieved.id == workspace.id
        assert retrieved.name == "Test Workspace"

    def test_get_nonexistent_workspace(self):
        """Test that DoesNotExist is raised for invalid ID."""
        with pytest.raises(Workspace.DoesNotExist):
            get_workspace_by_id_service(9999)


@pytest.mark.unit
class TestDeleteWorkspaceService:
    """Test cases for delete_workspace_service."""

    def test_delete_workspace(self, workspace_factory):
        """Test deleting a workspace."""
        workspace = workspace_factory()
        workspace_id = workspace.id

        result = delete_workspace_service(workspace_id)

        assert result is True
        assert not Workspace.objects.filter(id=workspace_id).exists()

    def test_delete_workspace_cascades_to_projects(
        self, workspace_factory, project_factory
    ):
        """Test that deleting workspace cascades to projects."""
        workspace = workspace_factory()
        project = project_factory(workspace=workspace)
        project_id = project.id

        delete_workspace_service(workspace.id)

        # Verify project was also deleted (cascade)
        from Projects.models import Project

        assert not Project.objects.filter(id=project_id).exists()

    def test_delete_nonexistent_workspace(self):
        """Test deleting nonexistent workspace raises error."""
        with pytest.raises(Workspace.DoesNotExist):
            delete_workspace_service(9999)
