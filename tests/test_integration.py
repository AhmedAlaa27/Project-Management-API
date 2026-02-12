"""
End-to-end integration tests for complete workflows.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from Workspaces.models import Workspace
from Projects.models import Project
from Tasks.models import Task

pytestmark = pytest.mark.django_db


@pytest.mark.integration
class TestCompleteWorkflow:
    """Test complete end-to-end workflows."""

    def test_create_workspace_project_task_workflow(
        self, authenticated_client, authenticated_user
    ):
        """Test complete workflow: create workspace -> project -> task."""
        # Step 1: Create workspace
        workspace_url = reverse("create_workspace")
        workspace_data = {
            "name": "My Workspace",
            "description": "Test workspace",
        }
        workspace_response = authenticated_client.post(
            workspace_url, workspace_data, format="json"
        )
        assert workspace_response.status_code == status.HTTP_201_CREATED
        workspace_id = workspace_response.data["data"]["id"]

        # Step 2: Create project in workspace
        project_url = reverse("create_project")
        deadline = timezone.now() + timedelta(days=30)
        project_data = {
            "name": "My Project",
            "description": "Test project",
            "workspace": workspace_id,
            "deadline": deadline.isoformat(),
        }
        project_response = authenticated_client.post(
            project_url, project_data, format="json"
        )
        assert project_response.status_code == status.HTTP_201_CREATED
        project_id = project_response.data["data"]["id"]

        # Step 3: Create task in project
        task_url = reverse("create_task")
        due_date = timezone.now() + timedelta(days=7)
        task_data = {
            "name": "My Task",
            "description": "Test task",
            "project": project_id,
            "status": "todo",
            "priority": "H",
            "due_date": due_date.isoformat(),
        }
        task_response = authenticated_client.post(task_url, task_data, format="json")
        assert task_response.status_code == status.HTTP_201_CREATED
        task_id = task_response.data["data"]["id"]

        # Verify all entities exist
        assert Workspace.objects.filter(id=workspace_id).exists()
        assert Project.objects.filter(id=project_id).exists()
        assert Task.objects.filter(id=task_id).exists()

        # Verify relationships
        task = Task.objects.get(id=task_id)
        assert task.project.id == project_id
        assert task.project.workspace.id == workspace_id
        assert task.author == authenticated_user

    def test_update_task_status_workflow(self, authenticated_client, task_factory):
        """Test workflow: create task -> update status to in_progress -> complete."""
        task = task_factory(status="todo")
        task_id = task.id
        url = reverse("update_task", kwargs={"task_id": task_id})

        # Update to in_progress
        response1 = authenticated_client.put(
            url, {"name": task.name, "status": "in_progress"}, format="json"
        )
        assert response1.status_code == status.HTTP_200_OK
        assert response1.data["data"]["status"] == "in_progress"

        # Update to done
        response2 = authenticated_client.put(
            url, {"name": task.name, "status": "done"}, format="json"
        )
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data["data"]["status"] == "done"

    def test_assign_and_reassign_task_workflow(
        self, authenticated_client, task_factory, user_factory
    ):
        """Test workflow: create task -> assign users -> reassign."""
        task = task_factory()
        user1 = user_factory()
        user2 = user_factory()
        user3 = user_factory()
        url = reverse("update_task", kwargs={"task_id": task.id})

        # Initial assignment
        response1 = authenticated_client.put(
            url,
            {"name": task.name, "assignee_ids": [user1.id, user2.id]},
            format="json",
        )
        assert response1.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.assignees.count() == 2

        # Reassignment
        response2 = authenticated_client.put(
            url, {"name": task.name, "assignee_ids": [user3.id]}, format="json"
        )
        assert response2.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.assignees.count() == 1
        assert user3 in task.assignees.all()

    def test_delete_cascade_workflow(
        self, authenticated_client, workspace_factory, project_factory, task_factory
    ):
        """Test workflow: create full hierarchy -> delete workspace -> verify cascade."""
        workspace = workspace_factory()
        project = project_factory(workspace=workspace)
        task = task_factory(project=project)

        workspace_id = workspace.id
        project_id = project.id
        task_id = task.id

        # Delete workspace
        url = reverse("delete_workspace", kwargs={"workspace_id": workspace_id})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

        # Verify cascade
        assert not Workspace.objects.filter(id=workspace_id).exists()
        assert not Project.objects.filter(id=project_id).exists()
        assert not Task.objects.filter(id=task_id).exists()


@pytest.mark.integration
class TestMultiUserWorkflow:
    """Test workflows involving multiple users."""

    def test_workspace_membership_workflow(
        self, authenticated_client, authenticated_user, workspace_factory, user_factory
    ):
        """Test workspace with multiple members."""
        workspace = workspace_factory(owner=authenticated_user)
        user2 = user_factory()
        user3 = user_factory()

        # Owner should be a member
        assert authenticated_user in workspace.members.all()

        # Add more members
        workspace.members.add(user2, user3)
        assert workspace.members.count() == 3

    def test_collaborative_task_workflow(
        self, authenticated_client, task_factory, user_factory
    ):
        """Test task assigned to multiple users."""
        user1 = user_factory()
        user2 = user_factory()
        user3 = user_factory()

        task = task_factory(assignees=[user1, user2, user3])

        assert task.assignees.count() == 3
        assert user1 in task.assignees.all()
        assert user2 in task.assignees.all()
        assert user3 in task.assignees.all()


@pytest.mark.integration
class TestFilteringWorkflow:
    """Test filtering across different endpoints."""

    def test_filter_projects_by_workspace(
        self, authenticated_client, workspace_factory, project_factory
    ):
        """Test filtering projects by workspace."""
        workspace1 = workspace_factory()
        workspace2 = workspace_factory()
        project_factory.create_batch(3, workspace=workspace1)
        project_factory.create_batch(2, workspace=workspace2)

        url = f"{reverse('project_list')}?workspace_id={workspace1.id}"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 3

    def test_filter_tasks_by_project(
        self, authenticated_client, project_factory, task_factory
    ):
        """Test filtering tasks by project."""
        project1 = project_factory()
        project2 = project_factory()
        task_factory.create_batch(4, project=project1)
        task_factory.create_batch(2, project=project2)

        url = f"{reverse('task_list')}?project_id={project1.id}"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 4

    def test_filter_user_workspaces(
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

    def test_filter_user_tasks(
        self, authenticated_client, authenticated_user, task_factory
    ):
        """Test filtering tasks by assigned user."""
        task_factory.create_batch(3, assignees=[authenticated_user])
        task_factory.create_batch(2)  # Not assigned to user

        url = f"{reverse('task_list')}?user_id={authenticated_user.id}"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 3


@pytest.mark.integration
class TestResponseFormat:
    """Test that all responses follow the standardized format."""

    def test_success_response_format(self, authenticated_client, workspace_factory):
        """Test success response format."""
        url = reverse("create_workspace")
        data = {"name": "Test Workspace"}

        response = authenticated_client.post(url, data, format="json")

        assert "success" in response.data
        assert "message" in response.data
        assert "data" in response.data
        assert response.data["success"] is True

    def test_error_response_format(self, authenticated_client):
        """Test error response format."""
        url = reverse("workspace_detail", kwargs={"workspace_id": 9999})

        response = authenticated_client.get(url)

        assert "success" in response.data
        assert "message" in response.data
        assert response.data["success"] is False

    def test_validation_error_response_format(self, authenticated_client):
        """Test validation error response format."""
        url = reverse("create_workspace")
        data = {}  # Missing required field

        response = authenticated_client.post(url, data, format="json")

        assert "success" in response.data
        assert "errors" in response.data
        assert response.data["success"] is False
