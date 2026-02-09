from django.db import transaction
from Projects.models import Project
from Workspaces.models import Workspace


def create_project_service(
    name: str, workspace_id: int, description: str = "", deadline=None
) -> Project:
    with transaction.atomic():
        workspace = Workspace.objects.get(id=workspace_id)
        project = Project.objects.create(
            name=name,
            workspace=workspace,
            description=description,
            deadline=deadline,
        )
        return project


def update_project_service(
    project_id: int, name: str, description: str = "", deadline=None
) -> Project:
    with transaction.atomic():
        project = Project.objects.get(id=project_id)
        project.name = name
        project.description = description
        project.deadline = deadline
        project.save()
        return project


def list_projects_service():
    return Project.objects.all()


def list_workspace_projects_service(workspace_id: int):
    return Project.objects.filter(workspace_id=workspace_id)


def get_project_by_id_service(project_id: int) -> Project:
    return Project.objects.get(id=project_id)


def delete_project_service(project_id: int) -> bool:
    with transaction.atomic():
        project = Project.objects.get(id=project_id)
        project.delete()
        return True
