import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import Any, cast

logger = logging.getLogger(__name__)

from Workspaces.serializers import (
    UpdateWorkspaceSerializer,
    WorkspaceSerializer,
    WorkspaceDetailSerializer,
)
from Workspaces.services import (
    create_workspace_service,
    delete_workspace_service,
    get_workspace_by_id_service,
    list_workspaces_service,
    update_workspace_service,
    user_list_workspaces_service,
)
from utils.responses import success_response, error_response, validation_error_response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_list(request: Request) -> Response:
    logger.debug(f"Workspace list requested by user: {request.user.id}")
    workspaces = list_workspaces_service()
    serializer = WorkspaceSerializer(workspaces, many=True)
    logger.info(f"Retrieved {len(workspaces)} workspaces")
    return success_response(
        data=serializer.data,
        message="Workspaces retrieved successfully",
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_workspace_list(request: Request) -> Response:
    logger.debug(f"User workspace list requested by user: {request.user.id}")
    workspaces = user_list_workspaces_service(request.user)
    serializer = WorkspaceSerializer(workspaces, many=True)
    logger.info(f"Retrieved {len(workspaces)} workspaces for user: {request.user.id}")
    return success_response(
        data=serializer.data,
        message="User workspaces retrieved successfully",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_workspace(request: Request) -> Response:
    logger.info(
        f"Create workspace request by user: {request.user.id} - name: {request.data.get('name')}"
    )
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
            logger.info(
                f"Workspace created successfully: {workspace.id} by user: {request.user.id}"
            )
            return success_response(
                data=response_serializer.data,
                message="Workspace created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Failed to create workspace - Error: {str(e)}")
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    logger.warning(f"Create workspace validation failed: {serializer.errors}")
    return validation_error_response(errors=serializer.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workspace_detail(request: Request, workspace_id: int) -> Response:
    logger.debug(
        f"Workspace detail requested for workspace_id: {workspace_id} by user: {request.user.id}"
    )
    try:
        workspace = get_workspace_by_id_service(workspace_id)
        serializer = WorkspaceDetailSerializer(workspace)
        logger.info(f"Workspace detail retrieved successfully: {workspace_id}")
        return success_response(
            data=serializer.data,
            message="Workspace retrieved successfully",
        )
    except Exception as e:
        logger.error(
            f"Failed to retrieve workspace detail for workspace_id: {workspace_id} - Error: {str(e)}"
        )
        return error_response(
            message=str(e),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_workspace(request: Request, workspace_id: int) -> Response:
    logger.info(
        f"Update workspace request for workspace_id: {workspace_id} by user: {request.user.id}"
    )
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
            logger.info(f"Workspace updated successfully: {workspace_id}")
            return success_response(
                data=response_serializer.data,
                message="Workspace updated successfully",
            )
        except Exception as e:
            logger.error(f"Failed to update workspace {workspace_id} - Error: {str(e)}")
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    logger.warning(
        f"Update workspace validation failed for workspace_id: {workspace_id} - Errors: {serializer.errors}"
    )
    return validation_error_response(errors=serializer.errors)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_workspace(request: Request, workspace_id: int) -> Response:
    logger.warning(
        f"Delete workspace request for workspace_id: {workspace_id} by user: {request.user.id}"
    )
    try:
        success = delete_workspace_service(workspace_id)
        if success:
            logger.info(f"Workspace deleted successfully: {workspace_id}")
            return success_response(
                message="Workspace deleted successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            logger.error(f"Failed to delete workspace: {workspace_id}")
            return error_response(
                message="Failed to delete workspace",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        logger.error(f"Error deleting workspace {workspace_id} - Error: {str(e)}")
        return error_response(
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
