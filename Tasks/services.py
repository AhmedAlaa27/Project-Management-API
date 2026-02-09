from django.db import transaction
from django.contrib.auth.models import AbstractUser
from Tasks.models import Task
from Projects.models import Project
from typing import Optional


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
    with transaction.atomic():
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
            task.assignees.set(assignee_ids)
        return task


def update_task_service(
    task_id: int,
    name: str,
    description: str = "",
    status: str = "todo",
    priority: str = "M",
    due_date=None,
    assignee_ids: Optional[list[int]] = None,
) -> Task:
    with transaction.atomic():
        task = Task.objects.get(id=task_id)
        task.name = name
        task.description = description
        task.status = status
        task.priority = priority
        task.due_date = due_date
        if assignee_ids is not None:
            task.assignees.set(assignee_ids)
        task.save()
        return task


def list_tasks_service():
    return Task.objects.all()


def list_project_tasks_service(project_id: int):
    return Task.objects.filter(project_id=project_id)


def list_user_tasks_service(user: AbstractUser):
    return Task.objects.filter(assignees=user)


def get_task_by_id_service(task_id: int) -> Task:
    return Task.objects.get(id=task_id)


def delete_task_service(task_id: int) -> bool:
    with transaction.atomic():
        task = Task.objects.get(id=task_id)
        task.delete()
        return True
