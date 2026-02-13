import logging
from django.db import transaction
from Projects.models import Project
from Workspaces.models import Workspace

logger = logging.getLogger(__name__)


def create_project_service(
    name: str, workspace_id: int, description: str = "", deadline=None
) -> Project:
    logger.info(f"Creating project: {name} in workspace: {workspace_id}")
    with transaction.atomic():
        try:
            workspace = Workspace.objects.get(id=workspace_id)
            project = Project.objects.create(
                name=name,
                workspace=workspace,
                description=description,
                deadline=deadline,
            )
            logger.info(f"Project created successfully: {project.id}")
            return project
        except Workspace.DoesNotExist:
            logger.error(f"Cannot create project - Workspace not found: {workspace_id}")
            raise
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            raise


def update_project_service(
    project_id: int, name: str, description: str = "", deadline=None
) -> Project:
    logger.info(f"Updating project: {project_id}")
    with transaction.atomic():
        try:
            project = Project.objects.get(id=project_id)
            project.name = name
            project.description = description
            project.deadline = deadline
            project.save()
            logger.info(f"Project updated successfully: {project_id}")
            return project
        except Project.DoesNotExist:
            logger.error(f"Cannot update - Project not found: {project_id}")
            raise
        except Exception as e:
            logger.error(f"Error updating project {project_id}: {str(e)}")
            raise


def list_projects_service():
    logger.debug("Fetching all projects")
    projects = Project.objects.all()
    logger.info("Projects retrieved successfully")
    return projects


def list_workspace_projects_service(workspace_id: int):
    logger.debug(f"Fetching projects for workspace: {workspace_id}")
    projects = Project.objects.filter(workspace_id=workspace_id)
    logger.info(f"Projects retrieved successfully for workspace: {workspace_id}")
    return projects


def get_project_by_id_service(project_id: int) -> Project:
    logger.debug(f"Fetching project by id: {project_id}")
    try:
        project = Project.objects.get(id=project_id)
        logger.info(f"Project found: {project_id}")
        return project
    except Project.DoesNotExist:
        logger.error(f"Project not found: {project_id}")
        raise


def delete_project_service(project_id: int) -> bool:
    logger.warning(f"Deleting project: {project_id}")
    with transaction.atomic():
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            logger.info(f"Project deleted successfully: {project_id}")
            return True
        except Project.DoesNotExist:
            logger.error(f"Cannot delete - Project not found: {project_id}")
            raise
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {str(e)}")
            raise
