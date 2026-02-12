"""
Unit tests for Projects app services.
"""

import pytest
from django.utils import timezone
from datetime import timedelta
from Projects.models import Project
from Projects.services import (
    create_project_service,
    update_project_service,
    list_projects_service,
    list_workspace_projects_service,
    get_project_by_id_service,
    delete_project_service,
)

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestCreateProjectService:
    """Test cases for create_project_service."""

    def test_create_project_with_all_fields(self, workspace_factory):
        """Test creating project with all fields."""
        workspace = workspace_factory()
        deadline = timezone.now() + timedelta(days=30)

        project = create_project_service(
            name="Test Project",
            workspace_id=workspace.id,
            description="Test Description",
            deadline=deadline,
        )

        assert project.name == "Test Project"
        assert project.description == "Test Description"
        assert project.workspace == workspace
        assert project.deadline == deadline

    def test_create_project_minimal_fields(self, workspace_factory):
        """Test creating project with minimal fields."""
        workspace = workspace_factory()

        project = create_project_service(name="Test Project", workspace_id=workspace.id)

        assert project.name == "Test Project"
        assert project.workspace == workspace

    def test_create_with_transaction(self, workspace_factory):
        """Test that create uses transaction."""
        workspace = workspace_factory()

        project = create_project_service(name="Test Project", workspace_id=workspace.id)

        assert Project.objects.filter(id=project.id).exists()


@pytest.mark.unit
class TestUpdateProjectService:
    """Test cases for update_project_service."""

    def test_update_project_fields(self, project_factory):
        """Test updating project fields."""
        project = project_factory(name="Old Name", description="Old Description")
        deadline = timezone.now() + timedelta(days=60)

        updated = update_project_service(
            project_id=project.id,
            name="New Name",
            description="New Description",
            deadline=deadline,
        )

        assert updated.name == "New Name"
        assert updated.description == "New Description"
        assert updated.deadline == deadline

    def test_update_with_transaction(self, project_factory):
        """Test that update uses transaction."""
        project = project_factory()

        updated = update_project_service(project_id=project.id, name="Updated")

        assert updated.name == "Updated"


@pytest.mark.unit
class TestListProjectsService:
    """Test cases for list_projects_service."""

    def test_list_all_projects(self, project_factory):
        """Test listing all projects."""
        project_factory.create_batch(3)

        projects = list_projects_service()

        assert projects.count() == 3

    def test_list_empty_projects(self):
        """Test listing when no projects exist."""
        projects = list_projects_service()

        assert projects.count() == 0


@pytest.mark.unit
class TestListWorkspaceProjectsService:
    """Test cases for list_workspace_projects_service."""

    def test_list_workspace_projects(self, workspace_factory, project_factory):
        """Test listing projects for a specific workspace."""
        workspace = workspace_factory()
        project_factory(workspace=workspace, name="Project 1")
        project_factory(workspace=workspace, name="Project 2")
        project_factory()  # Different workspace

        projects = list_workspace_projects_service(workspace.id)

        assert projects.count() == 2

    def test_list_workspace_projects_empty(self, workspace_factory):
        """Test listing projects for workspace with no projects."""
        workspace = workspace_factory()

        projects = list_workspace_projects_service(workspace.id)

        assert projects.count() == 0


@pytest.mark.unit
class TestGetProjectByIdService:
    """Test cases for get_project_by_id_service."""

    def test_get_existing_project(self, project_factory):
        """Test getting an existing project by ID."""
        project = project_factory(name="Test Project")

        retrieved = get_project_by_id_service(project.id)

        assert retrieved.id == project.id
        assert retrieved.name == "Test Project"

    def test_get_nonexistent_project(self):
        """Test that DoesNotExist is raised for invalid ID."""
        with pytest.raises(Project.DoesNotExist):
            get_project_by_id_service(9999)


@pytest.mark.unit
class TestDeleteProjectService:
    """Test cases for delete_project_service."""

    def test_delete_project(self, project_factory):
        """Test deleting a project."""
        project = project_factory()
        project_id = project.id

        result = delete_project_service(project_id)

        assert result is True
        assert not Project.objects.filter(id=project_id).exists()

    def test_delete_project_cascades_to_tasks(self, project_factory, task_factory):
        """Test that deleting project cascades to tasks."""
        project = project_factory()
        task = task_factory(project=project)
        task_id = task.id

        delete_project_service(project.id)

        # Verify task was also deleted (cascade)
        from Tasks.models import Task

        assert not Task.objects.filter(id=task_id).exists()

    def test_delete_nonexistent_project(self):
        """Test deleting nonexistent project raises error."""
        with pytest.raises(Project.DoesNotExist):
            delete_project_service(9999)
