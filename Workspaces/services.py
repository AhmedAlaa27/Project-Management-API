from django.db import transaction
from Workspaces.models import Workspace
from django.contrib.auth.models import AbstractUser


def create_workspace_service(
    name: str, owner: AbstractUser, description: str = ""
) -> Workspace:
    with transaction.atomic():
        workspace = Workspace.objects.create(
            name=name, owner=owner, description=description
        )
        workspace.members.add(owner)
        return workspace


def update_workspace_service(
    workspace_id: int, name: str, description: str = ""
) -> Workspace:
    with transaction.atomic():
        workspace = Workspace.objects.get(id=workspace_id)
        workspace.name = name
        workspace.description = description
        workspace.save()
        return workspace


def list_workspaces_service():
    return Workspace.objects.all()


def user_list_workspaces_service(user: AbstractUser):
    return Workspace.objects.filter(members=user)


def get_workspace_by_id_service(workspace_id: int) -> Workspace:
    return Workspace.objects.get(id=workspace_id)


def delete_workspace_service(workspace_id: int) -> bool:
    with transaction.atomic():
        workspace = Workspace.objects.get(id=workspace_id)
        workspace.delete()
        return True
    return False
