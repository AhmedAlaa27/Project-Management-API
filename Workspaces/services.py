import logging
from django.db import transaction
from Workspaces.models import Workspace
from django.contrib.auth.models import AbstractUser

logger = logging.getLogger(__name__)


def create_workspace_service(
    name: str, owner: AbstractUser, description: str = ""
) -> Workspace:
    logger.info(f"Creating workspace: {name} for owner: {owner.id}")
    with transaction.atomic():
        try:
            workspace = Workspace.objects.create(
                name=name, owner=owner, description=description
            )
            workspace.members.add(owner)
            logger.info(f"Workspace created successfully: {workspace.id}")
            return workspace
        except Exception as e:
            logger.error(f"Error creating workspace: {str(e)}")
            raise


def update_workspace_service(
    workspace_id: int, name: str, description: str = ""
) -> Workspace:
    logger.info(f"Updating workspace: {workspace_id}")
    with transaction.atomic():
        try:
            workspace = Workspace.objects.get(id=workspace_id)
            workspace.name = name
            workspace.description = description
            workspace.save()
            logger.info(f"Workspace updated successfully: {workspace_id}")
            return workspace
        except Workspace.DoesNotExist:
            logger.error(f"Cannot update - Workspace not found: {workspace_id}")
            raise
        except Exception as e:
            logger.error(f"Error updating workspace {workspace_id}: {str(e)}")
            raise


def list_workspaces_service():
    logger.debug("Fetching all workspaces")
    workspaces = Workspace.objects.all()
    logger.info("Workspaces retrieved successfully")
    return workspaces


def user_list_workspaces_service(user: AbstractUser):
    logger.debug(f"Fetching workspaces for user: {user.id}")
    workspaces = Workspace.objects.filter(members=user)
    logger.info(f"Workspaces retrieved successfully for user: {user.id}")
    return workspaces


def get_workspace_by_id_service(workspace_id: int) -> Workspace:
    logger.debug(f"Fetching workspace by id: {workspace_id}")
    try:
        workspace = Workspace.objects.get(id=workspace_id)
        logger.info(f"Workspace found: {workspace_id}")
        return workspace
    except Workspace.DoesNotExist:
        logger.error(f"Workspace not found: {workspace_id}")
        raise


def delete_workspace_service(workspace_id: int) -> bool:
    logger.warning(f"Deleting workspace: {workspace_id}")
    with transaction.atomic():
        try:
            workspace = Workspace.objects.get(id=workspace_id)
            workspace.delete()
            logger.info(f"Workspace deleted successfully: {workspace_id}")
            return True
        except Workspace.DoesNotExist:
            logger.error(f"Cannot delete - Workspace not found: {workspace_id}")
            raise
        except Exception as e:
            logger.error(f"Error deleting workspace {workspace_id}: {str(e)}")
            raise
    return False
