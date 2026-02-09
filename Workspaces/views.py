from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import Any, cast

from Workspaces.serializers import UpdateWorkspaceSerializer, WorkspaceSerializer
from Workspaces.services import (
    create_workspace_service,
    delete_workspace_service,
    get_workspace_by_id_service,
    list_workspaces_service,
    update_workspace_service,
    user_list_workspaces_service,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_list(request: Request) -> Response:
    workspaces = list_workspaces_service()
    serializer = WorkspaceSerializer(workspaces, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_workspace_list(request: Request) -> Response:
    workspaces = user_list_workspaces_service(request.user)
    serializer = WorkspaceSerializer(workspaces, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_workspace(request: Request) -> Response:
    serializer = WorkspaceSerializer(data=request.data)
    if serializer.is_valid():
        try:
            data = cast(dict[str, Any], serializer.validated_data)
            workspace = create_workspace_service(
                name=data["name"],
                description=data.get("description", ""),
                owner=request.user,
            )
            response_serializer = WorkspaceSerializer(workspace)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_detail(request: Request, workspace_id: int) -> Response:
    workspace = get_workspace_by_id_service(workspace_id)
    serializer = WorkspaceSerializer(workspace, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_workspace(request: Request, workspace_id: int) -> Response:
    serializer = UpdateWorkspaceSerializer(data=request.data)
    if serializer.is_valid():
        try:
            data = cast(dict[str, Any], serializer.validated_data)
            workspace = update_workspace_service(
                workspace_id=workspace_id,
                name=data["name"],
                description=data.get("description", ""),
            )
            response_serializer = WorkspaceSerializer(workspace)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_workspace(request: Request, workspace_id: int) -> Response:
    try:
        success = delete_workspace_service(workspace_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "Failed to delete workspace."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
