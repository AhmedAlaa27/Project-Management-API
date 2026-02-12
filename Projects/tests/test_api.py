"""
Integration tests for Projects app API endpoints.
"""

import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from Projects.models import Project

pytestmark = pytest.mark.django_db


@pytest.mark.integration
class TestCreateProjectAPI:
    """Test cases for project creation endpoint."""

    def test_create_project_authenticated(
        self, authenticated_client, workspace_factory
    ):
        """Test creating project with authentication."""
        workspace = workspace_factory()
        url = reverse("create_project")
        deadline = timezone.now() + timedelta(days=30)
        data = {
            "name": "New Project",
            "description": "New Description",
            "workspace": workspace.id,
            "deadline": deadline.isoformat(),
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["data"]["name"] == "New Project"
        assert Project.objects.filter(name="New Project").exists()

    def test_create_project_minimal_fields(
        self, authenticated_client, workspace_factory
    ):
        """Test creating project with minimal required fields."""
        workspace = workspace_factory()
        url = reverse("create_project")
        data = {
            "name": "New Project",
            "workspace": workspace.id,
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_project_invalid_workspace(self, authenticated_client):
        """Test creating project with invalid workspace ID."""
        url = reverse("create_project")
        data = {
            "name": "New Project",
            "workspace": 9999,
        }

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_project_unauthenticated(self, api_client, workspace_factory):
        """Test creating project fails without authentication."""
        workspace = workspace_factory()
        url = reverse("create_project")
        data = {
            "name": "New Project",
            "workspace": workspace.id,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_project_missing_name(self, authenticated_client, workspace_factory):
        """Test creating project without name fails."""
        workspace = workspace_factory()
        url = reverse("create_project")
        data = {"workspace": workspace.id}

        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
class TestListProjectsAPI:
    """Test cases for listing projects."""

    def test_list_all_projects(self, authenticated_client, project_factory):
        """Test listing all projects."""
        project_factory.create_batch(3)
        url = reverse("project_list")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]) >= 3

    def test_list_projects_filtered_by_workspace(
        self, authenticated_client, workspace_factory, project_factory
    ):
        """Test filtering projects by workspace."""
        workspace = workspace_factory()
        project_factory(workspace=workspace)
        project_factory(workspace=workspace)
        project_factory()  # Different workspace
        url = f"{reverse('project_list')}?workspace_id={workspace.id}"

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2

    def test_list_projects_unauthenticated(self, api_client):
        """Test listing projects fails without authentication."""
        url = reverse("project_list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestProjectDetailAPI:
    """Test cases for project detail endpoint."""

    def test_get_project_detail_with_tasks(
        self, authenticated_client, project_factory, task_factory
    ):
        """Test getting project details with nested tasks."""
        project = project_factory()
        task_factory(project=project, name="Task 1")
        task_factory(project=project, name="Task 2")
        url = reverse("project_detail", kwargs={"project_id": project.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert "tasks" in response.data["data"]
        assert len(response.data["data"]["tasks"]) == 2

    def test_get_project_detail_unauthenticated(self, api_client, project_factory):
        """Test getting project detail fails without authentication."""
        project = project_factory()
        url = reverse("project_detail", kwargs={"project_id": project.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_nonexistent_project(self, authenticated_client):
        """Test getting nonexistent project."""
        url = reverse("project_detail", kwargs={"project_id": 9999})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
class TestUpdateProjectAPI:
    """Test cases for updating project."""

    def test_update_project_authenticated(self, authenticated_client, project_factory):
        """Test updating project with authentication."""
        project = project_factory(name="Old Name", description="Old Desc")
        url = reverse("update_project", kwargs={"project_id": project.id})
        deadline = timezone.now() + timedelta(days=60)
        data = {
            "name": "New Name",
            "description": "New Description",
            "deadline": deadline.isoformat(),
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["name"] == "New Name"

    def test_update_project_partial(self, authenticated_client, project_factory):
        """Test partial update of project."""
        project = project_factory(name="Original", description="Original Desc")
        url = reverse("update_project", kwargs={"project_id": project.id})
        data = {"name": "Updated Name"}

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["name"] == "Updated Name"

    def test_update_project_unauthenticated(self, api_client, project_factory):
        """Test updating project fails without authentication."""
        project = project_factory()
        url = reverse("update_project", kwargs={"project_id": project.id})
        data = {"name": "New Name"}

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestDeleteProjectAPI:
    """Test cases for deleting project."""

    def test_delete_project_authenticated(self, authenticated_client, project_factory):
        """Test deleting project with authentication."""
        project = project_factory()
        url = reverse("delete_project", kwargs={"project_id": project.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert not Project.objects.filter(id=project.id).exists()

    def test_delete_project_cascades_to_tasks(
        self, authenticated_client, project_factory, task_factory
    ):
        """Test that deleting project cascades to tasks."""
        project = project_factory()
        task = task_factory(project=project)
        task_id = task.id
        url = reverse("delete_project", kwargs={"project_id": project.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        from Tasks.models import Task

        assert not Task.objects.filter(id=task_id).exists()

    def test_delete_project_unauthenticated(self, api_client, project_factory):
        """Test deleting project fails without authentication."""
        project = project_factory()
        url = reverse("delete_project", kwargs={"project_id": project.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_nonexistent_project(self, authenticated_client):
        """Test deleting nonexistent project."""
        url = reverse("delete_project", kwargs={"project_id": 9999})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
