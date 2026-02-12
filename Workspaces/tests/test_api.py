"""
Integration tests for Workspaces app API endpoints.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from Workspaces.models import Workspace

pytestmark = pytest.mark.django_db


@pytest.mark.integration
class TestCreateWorkspaceAPI:
    """Test cases for workspace creation endpoint."""

    def test_create_workspace_authenticated(
        self, authenticated_client, authenticated_user
    ):
        """Test creating workspace with authentication."""
        url = reverse("create_workspace")
        data = {
            "name": "New Workspace",
            "description": "New Description",
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["data"]["name"] == "New Workspace"
        # Verify workspace exists in database
        assert Workspace.objects.filter(name="New Workspace").exists()

    def test_create_workspace_owner_added_to_members(
        self, authenticated_client, authenticated_user
    ):
        """Test that owner is automatically added to members."""
        url = reverse("create_workspace")
        data = {"name": "Test Workspace"}

        response = authenticated_client.post(url, data, format="json")

        workspace = Workspace.objects.get(id=response.data["data"]["id"])
        assert authenticated_user in workspace.members.all()

    def test_create_workspace_unauthenticated(self, api_client):
        """Test creating workspace fails without authentication."""
        url = reverse("create_workspace")
        data = {"name": "Test Workspace"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_workspace_missing_name(self, authenticated_client):
        """Test creating workspace without name fails."""
        url = reverse("create_workspace")
        data = {"description": "Only description"}

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
class TestListWorkspacesAPI:
    """Test cases for listing workspaces."""

    def test_list_all_workspaces(self, authenticated_client, workspace_factory):
        """Test listing all workspaces."""
        workspace_factory.create_batch(3)
        url = reverse("workspace_list")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]) >= 3

    def test_list_user_workspaces(
        self, authenticated_client, authenticated_user, workspace_factory
    ):
        """Test listing only user's workspaces."""
        workspace_factory(members=[authenticated_user])
        workspace_factory(members=[authenticated_user])
        workspace_factory()  # Not a member
        url = reverse("user_workspace_list")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2

    def test_list_workspaces_unauthenticated(self, api_client):
        """Test listing workspaces fails without authentication."""
        url = reverse("workspace_list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestWorkspaceDetailAPI:
    """Test cases for workspace detail endpoint."""

    def test_get_workspace_detail_with_projects(
        self, authenticated_client, workspace_factory, project_factory
    ):
        """Test getting workspace details with nested projects."""
        workspace = workspace_factory()
        project_factory(workspace=workspace, name="Project 1")
        project_factory(workspace=workspace, name="Project 2")
        url = reverse("workspace_detail", kwargs={"workspace_id": workspace.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert "projects" in response.data["data"]
        assert len(response.data["data"]["projects"]) == 2

    def test_get_workspace_detail_unauthenticated(self, api_client, workspace_factory):
        """Test getting workspace detail fails without authentication."""
        workspace = workspace_factory()
        url = reverse("workspace_detail", kwargs={"workspace_id": workspace.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_nonexistent_workspace(self, authenticated_client):
        """Test getting nonexistent workspace."""
        url = reverse("workspace_detail", kwargs={"workspace_id": 9999})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
class TestUpdateWorkspaceAPI:
    """Test cases for updating workspace."""

    def test_update_workspace_authenticated(
        self, authenticated_client, workspace_factory
    ):
        """Test updating workspace with authentication."""
        workspace = workspace_factory(name="Old Name", description="Old Desc")
        url = reverse("update_workspace", kwargs={"workspace_id": workspace.id})
        data = {
            "name": "New Name",
            "description": "New Description",
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["name"] == "New Name"
        assert response.data["data"]["description"] == "New Description"

    def test_update_workspace_partial(self, authenticated_client, workspace_factory):
        """Test partial update of workspace."""
        workspace = workspace_factory(name="Original", description="Original Desc")
        url = reverse("update_workspace", kwargs={"workspace_id": workspace.id})
        data = {"name": "Updated Name"}

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["name"] == "Updated Name"

    def test_update_workspace_unauthenticated(self, api_client, workspace_factory):
        """Test updating workspace fails without authentication."""
        workspace = workspace_factory()
        url = reverse("update_workspace", kwargs={"workspace_id": workspace.id})
        data = {"name": "New Name"}

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestDeleteWorkspaceAPI:
    """Test cases for deleting workspace."""

    def test_delete_workspace_authenticated(
        self, authenticated_client, workspace_factory
    ):
        """Test deleting workspace with authentication."""
        workspace = workspace_factory()
        url = reverse("delete_workspace", kwargs={"workspace_id": workspace.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert not Workspace.objects.filter(id=workspace.id).exists()

    def test_delete_workspace_cascades_to_projects(
        self, authenticated_client, workspace_factory, project_factory
    ):
        """Test that deleting workspace cascades to projects."""
        workspace = workspace_factory()
        project = project_factory(workspace=workspace)
        project_id = project.id
        url = reverse("delete_workspace", kwargs={"workspace_id": workspace.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        # Verify project was deleted
        from Projects.models import Project

        assert not Project.objects.filter(id=project_id).exists()

    def test_delete_workspace_unauthenticated(self, api_client, workspace_factory):
        """Test deleting workspace fails without authentication."""
        workspace = workspace_factory()
        url = reverse("delete_workspace", kwargs={"workspace_id": workspace.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_nonexistent_workspace(self, authenticated_client):
        """Test deleting nonexistent workspace."""
        url = reverse("delete_workspace", kwargs={"workspace_id": 9999})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
