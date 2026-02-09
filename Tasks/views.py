from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import Any, cast

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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_list(request: Request) -> Response:
    project_id = request.query_params.get("project_id")
    user_id = request.query_params.get("user_id")

    if project_id:
        tasks = list_project_tasks_service(int(project_id))
    elif user_id:
        tasks = list_user_tasks_service(request.user)
    else:
        tasks = list_tasks_service()

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request: Request) -> Response:
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
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_detail(request: Request, task_id: int) -> Response:
    try:
        task = get_task_by_id_service(task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_task(request: Request, task_id: int) -> Response:
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
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request: Request, task_id: int) -> Response:
    try:
        success = delete_task_service(task_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "Failed to delete task."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
