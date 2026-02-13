import logging
from django.db import transaction
from django.contrib.auth.models import AbstractUser
from Tasks.models import Task
from Projects.models import Project
from typing import Optional

logger = logging.getLogger(__name__)


def create_task_service(
    name: str,
    project_id: int,
    author: AbstractUser,
    description: str = "",
    status: str = "todo",
    priority: str = "M",
    due_date=None,
    assignee_ids: Optional[list[int]] = None,
) -> Task:
    logger.info(
        f"Creating task: {name} in project: {project_id} by author: {author.id}"
    )
    with transaction.atomic():
        try:
            project = Project.objects.get(id=project_id)
            task = Task.objects.create(
                name=name,
                project=project,
                author=author,
                description=description,
                status=status,
                priority=priority,
                due_date=due_date,
            )
            if assignee_ids:
                logger.debug(f"Assigning task {task.id} to users: {assignee_ids}")
                task.assignees.set(assignee_ids)
            logger.info(f"Task created successfully: {task.id}")
            return task
        except Project.DoesNotExist:
            logger.error(f"Cannot create task - Project not found: {project_id}")
            raise
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            raise


def update_task_service(
    task_id: int,
    name: str,
    description: str = "",
    status: str = "todo",
    priority: str = "M",
    due_date=None,
    assignee_ids: Optional[list[int]] = None,
) -> Task:
    logger.info(f"Updating task: {task_id}")
    with transaction.atomic():
        try:
            task = Task.objects.get(id=task_id)
            task.name = name
            task.description = description
            task.status = status
            task.priority = priority
            task.due_date = due_date
            if assignee_ids is not None:
                logger.debug(f"Updating assignees for task {task_id}: {assignee_ids}")
                task.assignees.set(assignee_ids)
            task.save()
            logger.info(f"Task updated successfully: {task_id}")
            return task
        except Task.DoesNotExist:
            logger.error(f"Cannot update - Task not found: {task_id}")
            raise
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {str(e)}")
            raise


def list_tasks_service():
    logger.debug("Fetching all tasks")
    tasks = Task.objects.all()
    logger.info("Tasks retrieved successfully")
    return tasks


def list_project_tasks_service(project_id: int):
    logger.debug(f"Fetching tasks for project: {project_id}")
    tasks = Task.objects.filter(project_id=project_id)
    logger.info(f"Tasks retrieved successfully for project: {project_id}")
    return tasks


def list_user_tasks_service(user: AbstractUser):
    logger.debug(f"Fetching tasks for user: {user.id}")
    tasks = Task.objects.filter(assignees=user)
    logger.info(f"Tasks retrieved successfully for user: {user.id}")
    return tasks


def get_task_by_id_service(task_id: int) -> Task:
    logger.debug(f"Fetching task by id: {task_id}")
    try:
        task = Task.objects.get(id=task_id)
        logger.info(f"Task found: {task_id}")
        return task
    except Task.DoesNotExist:
        logger.error(f"Task not found: {task_id}")
        raise


def delete_task_service(task_id: int) -> bool:
    logger.warning(f"Deleting task: {task_id}")
    with transaction.atomic():
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            logger.info(f"Task deleted successfully: {task_id}")
            return True
        except Task.DoesNotExist:
            logger.error(f"Cannot delete - Task not found: {task_id}")
            raise
        except Exception as e:
            logger.error(f"Error deleting task {task_id}: {str(e)}")
            raise
