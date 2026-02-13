import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import Any, cast

logger = logging.getLogger(__name__)

from Tasks.serializers import (
    CreateTaskSerializer,
    TaskSerializer,
    UpdateTaskSerializer,
)
from Tasks.services import (
    create_task_service,
    delete_task_service,
    get_task_by_id_service,
    list_project_tasks_service,
    list_tasks_service,
    list_user_tasks_service,
    update_task_service,
)
from utils.responses import success_response, error_response, validation_error_response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_list(request: Request) -> Response:
    project_id = request.query_params.get("project_id")
    user_id = request.query_params.get("user_id")
    logger.debug(
        f"Task list requested by user: {request.user.id}, project_id: {project_id}, user_id: {user_id}"
    )

    if project_id:
        tasks = list_project_tasks_service(int(project_id))
    elif user_id:
        tasks = list_user_tasks_service(request.user)
    else:
        tasks = list_tasks_service()

    serializer = TaskSerializer(tasks, many=True)
    logger.info(f"Retrieved {len(tasks)} tasks")
    return success_response(
        data=serializer.data,
        message="Tasks retrieved successfully",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request: Request) -> Response:
    logger.info(
        f"Create task request by user: {request.user.id} - name: {request.data.get('name')}"
    )
    serializer = CreateTaskSerializer(data=request.data)
    if serializer.is_valid():
        try:
            data = cast(dict[str, Any], serializer.validated_data)
            task = create_task_service(
                name=data["name"],
                project_id=data["project"].id,
                author=request.user,
                description=data.get("description", ""),
                status=data.get("status", "todo"),
                priority=data.get("priority", "M"),
                due_date=data.get("due_date"),
                assignee_ids=data.get("assignee_ids"),
            )
            response_serializer = TaskSerializer(task)
            logger.info(
                f"Task created successfully: {task.id} by user: {request.user.id}"
            )
            return success_response(
                data=response_serializer.data,
                message="Task created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Failed to create task - Error: {str(e)}")
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    logger.warning(f"Create task validation failed: {serializer.errors}")
    return validation_error_response(errors=serializer.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_detail(request: Request, task_id: int) -> Response:
    logger.debug(
        f"Task detail requested for task_id: {task_id} by user: {request.user.id}"
    )
    try:
        task = get_task_by_id_service(task_id)
        serializer = TaskSerializer(task)
        logger.info(f"Task detail retrieved successfully: {task_id}")
        return success_response(
            data=serializer.data,
            message="Task retrieved successfully",
        )
    except Exception as e:
        logger.error(
            f"Failed to retrieve task detail for task_id: {task_id} - Error: {str(e)}"
        )
        return error_response(
            message=str(e),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_task(request: Request, task_id: int) -> Response:
    logger.info(
        f"Update task request for task_id: {task_id} by user: {request.user.id}"
    )
    serializer = UpdateTaskSerializer(data=request.data)
    if serializer.is_valid():
        try:
            data = cast(dict[str, Any], serializer.validated_data)
            task = update_task_service(
                task_id=task_id,
                name=data["name"],
                description=data.get("description", ""),
                status=data.get("status", "todo"),
                priority=data.get("priority", "M"),
                due_date=data.get("due_date"),
                assignee_ids=data.get("assignee_ids"),
            )
            response_serializer = TaskSerializer(task)
            logger.info(f"Task updated successfully: {task_id}")
            return success_response(
                data=response_serializer.data,
                message="Task updated successfully",
            )
        except Exception as e:
            logger.error(f"Failed to update task {task_id} - Error: {str(e)}")
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    logger.warning(
        f"Update task validation failed for task_id: {task_id} - Errors: {serializer.errors}"
    )
    return validation_error_response(errors=serializer.errors)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request: Request, task_id: int) -> Response:
    logger.warning(
        f"Delete task request for task_id: {task_id} by user: {request.user.id}"
    )
    try:
        success = delete_task_service(task_id)
        if success:
            logger.info(f"Task deleted successfully: {task_id}")
            return success_response(
                message="Task deleted successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            logger.error(f"Failed to delete task: {task_id}")
            return error_response(
                message="Failed to delete task",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        logger.error(f"Error deleting task {task_id} - Error: {str(e)}")
        return error_response(
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
