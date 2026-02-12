"""
Integration tests for cascade delete behavior across entities.
"""

import pytest
from Workspaces.models import Workspace
from Projects.models import Project
from Tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.integration
class TestCascadeDeleteWorkspace:
    """Test cascade delete behavior when deleting a workspace."""

    def test_delete_workspace_cascades_to_projects(
        self, workspace_factory, project_factory
    ):
        """Test that deleting workspace cascades to all projects."""
        workspace = workspace_factory()
        project1 = project_factory(workspace=workspace)
        project2 = project_factory(workspace=workspace)
        project1_id = project1.id
        project2_id = project2.id

        workspace.delete()

        # Projects should be deleted
        assert not Project.objects.filter(id=project1_id).exists()
        assert not Project.objects.filter(id=project2_id).exists()

    def test_delete_workspace_cascades_to_tasks(
        self, workspace_factory, project_factory, task_factory
    ):
        """Test that deleting workspace cascades through projects to tasks."""
        workspace = workspace_factory()
        project = project_factory(workspace=workspace)
        task1 = task_factory(project=project)
        task2 = task_factory(project=project)
        task1_id = task1.id
        task2_id = task2.id

        workspace.delete()

        # Tasks should be deleted through cascade
        assert not Task.objects.filter(id=task1_id).exists()
        assert not Task.objects.filter(id=task2_id).exists()

    def test_delete_workspace_full_cascade_chain(
        self, workspace_factory, project_factory, task_factory
    ):
        """Test complete cascade: workspace -> projects -> tasks."""
        workspace = workspace_factory()
        project1 = project_factory(workspace=workspace)
        project2 = project_factory(workspace=workspace)
        task1 = task_factory(project=project1)
        task2 = task_factory(project=project1)
        task3 = task_factory(project=project2)

        workspace_id = workspace.id
        project1_id = project1.id
        project2_id = project2.id
        task1_id = task1.id
        task2_id = task2.id
        task3_id = task3.id

        workspace.delete()

        # Verify all entities are deleted
        assert not Workspace.objects.filter(id=workspace_id).exists()
        assert not Project.objects.filter(id=project1_id).exists()
        assert not Project.objects.filter(id=project2_id).exists()
        assert not Task.objects.filter(id=task1_id).exists()
        assert not Task.objects.filter(id=task2_id).exists()
        assert not Task.objects.filter(id=task3_id).exists()


@pytest.mark.integration
class TestCascadeDeleteProject:
    """Test cascade delete behavior when deleting a project."""

    def test_delete_project_cascades_to_tasks(self, project_factory, task_factory):
        """Test that deleting project cascades to all tasks."""
        project = project_factory()
        task1 = task_factory(project=project)
        task2 = task_factory(project=project)
        task1_id = task1.id
        task2_id = task2.id

        project.delete()

        # Tasks should be deleted
        assert not Task.objects.filter(id=task1_id).exists()
        assert not Task.objects.filter(id=task2_id).exists()

    def test_delete_project_preserves_workspace(
        self, workspace_factory, project_factory
    ):
        """Test that deleting project does not delete workspace."""
        workspace = workspace_factory()
        project = project_factory(workspace=workspace)
        workspace_id = workspace.id

        project.delete()

        # Workspace should still exist
        assert Workspace.objects.filter(id=workspace_id).exists()


@pytest.mark.integration
class TestCascadeDeleteUser:
    """Test cascade delete behavior when deleting a user."""

    def test_delete_user_cascades_owned_workspaces(
        self, user_factory, workspace_factory
    ):
        """Test that deleting user cascades to owned workspaces."""
        user = user_factory()
        workspace = workspace_factory(owner=user)
        workspace_id = workspace.id

        user.delete()

        # Owned workspace should be deleted
        assert not Workspace.objects.filter(id=workspace_id).exists()

    def test_delete_user_cascades_through_workspace_to_projects(
        self, user_factory, workspace_factory, project_factory
    ):
        """Test that deleting user cascades through workspace to projects."""
        user = user_factory()
        workspace = workspace_factory(owner=user)
        project = project_factory(workspace=workspace)
        project_id = project.id

        user.delete()

        # Project should be deleted through workspace cascade
        assert not Project.objects.filter(id=project_id).exists()

    def test_delete_user_full_cascade_chain(
        self, user_factory, workspace_factory, project_factory, task_factory
    ):
        """Test complete cascade: user -> workspace -> projects -> tasks."""
        user = user_factory()
        workspace = workspace_factory(owner=user)
        project = project_factory(workspace=workspace)
        task = task_factory(project=project)

        workspace_id = workspace.id
        project_id = project.id
        task_id = task.id

        user.delete()

        # Verify all entities are deleted
        assert not Workspace.objects.filter(id=workspace_id).exists()
        assert not Project.objects.filter(id=project_id).exists()
        assert not Task.objects.filter(id=task_id).exists()


@pytest.mark.integration
class TestTaskAuthorDeletion:
    """Test SET_NULL behavior when task author is deleted."""

    def test_delete_author_sets_task_author_to_null(self, user_factory, task_factory):
        """Test that deleting task author sets author field to NULL."""
        author = user_factory()
        task = task_factory(author=author)
        task_id = task.id

        author.delete()

        # Task should still exist with author set to NULL
        assert Task.objects.filter(id=task_id).exists()
        task.refresh_from_db()
        assert task.author is None

    def test_delete_author_preserves_multiple_tasks(self, user_factory, task_factory):
        """Test that deleting author preserves all their tasks."""
        author = user_factory()
        task1 = task_factory(author=author)
        task2 = task_factory(author=author)
        task3 = task_factory(author=author)

        task1_id = task1.id
        task2_id = task2.id
        task3_id = task3.id

        author.delete()

        # All tasks should still exist
        assert Task.objects.filter(id=task1_id).exists()
        assert Task.objects.filter(id=task2_id).exists()
        assert Task.objects.filter(id=task3_id).exists()

        # All should have NULL author
        task1.refresh_from_db()
        task2.refresh_from_db()
        task3.refresh_from_db()
        assert task1.author is None
        assert task2.author is None
        assert task3.author is None

    def test_delete_assignee_removes_from_tasks(self, user_factory, task_factory):
        """Test that deleting a user removes them from task assignees."""
        user = user_factory()
        task1 = task_factory(assignees=[user])
        task2 = task_factory(assignees=[user])

        user.delete()

        # Tasks should still exist but user should be removed from assignees
        task1.refresh_from_db()
        task2.refresh_from_db()
        assert user not in task1.assignees.all()
        assert user not in task2.assignees.all()


@pytest.mark.integration
class TestMultipleCascades:
    """Test complex scenarios with multiple cascades."""

    def test_delete_workspace_owner_cascades_everything(
        self, user_factory, workspace_factory, project_factory, task_factory
    ):
        """Test deleting workspace owner cascades to all owned entities."""
        owner = user_factory()
        workspace1 = workspace_factory(owner=owner)
        workspace2 = workspace_factory(owner=owner)
        project1 = project_factory(workspace=workspace1)
        project2 = project_factory(workspace=workspace2)
        task1 = task_factory(project=project1)
        task2 = task_factory(project=project2)

        owner.delete()

        # Everything should be deleted
        assert not Workspace.objects.filter(owner_id=owner.id).exists()
        assert not Project.objects.filter(id=project1.id).exists()
        assert not Project.objects.filter(id=project2.id).exists()
        assert not Task.objects.filter(id=task1.id).exists()
        assert not Task.objects.filter(id=task2.id).exists()

    def test_delete_workspace_preserves_other_workspaces(
        self, workspace_factory, project_factory, task_factory
    ):
        """Test that deleting one workspace doesn't affect others."""
        workspace1 = workspace_factory()
        workspace2 = workspace_factory()
        project1 = project_factory(workspace=workspace1)
        project2 = project_factory(workspace=workspace2)
        task1 = task_factory(project=project1)
        task2 = task_factory(project=project2)

        workspace1.delete()

        # Workspace2 and its entities should still exist
        assert Workspace.objects.filter(id=workspace2.id).exists()
        assert Project.objects.filter(id=project2.id).exists()
        assert Task.objects.filter(id=task2.id).exists()

        # Workspace1 and its entities should be deleted
        assert not Workspace.objects.filter(id=workspace1.id).exists()
        assert not Project.objects.filter(id=project1.id).exists()
        assert not Task.objects.filter(id=task1.id).exists()
