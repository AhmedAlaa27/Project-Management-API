import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import Any, cast

logger = logging.getLogger(__name__)

from Projects.serializers import (
    CreateProjectSerializer,
    ProjectSerializer,
    ProjectDetailSerializer,
    UpdateProjectSerializer,
)
from Projects.services import (
    create_project_service,
    delete_project_service,
    get_project_by_id_service,
    list_projects_service,
    list_workspace_projects_service,
    update_project_service,
)
from utils.responses import success_response, error_response, validation_error_response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def project_list(request: Request) -> Response:
    workspace_id = request.query_params.get("workspace_id")
    logger.debug(
        f"Project list requested by user: {request.user.id}, workspace_id: {workspace_id}"
    )
    if workspace_id:
        projects = list_workspace_projects_service(int(workspace_id))
    else:
        projects = list_projects_service()
    serializer = ProjectSerializer(projects, many=True)
    logger.info(f"Retrieved {len(projects)} projects")
    return success_response(
        data=serializer.data,
        message="Projects retrieved successfully",
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_project(request: Request) -> Response:
    logger.info(
        f"Create project request by user: {request.user.id} - name: {request.data.get('name')}"
    )
    serializer = CreateProjectSerializer(data=request.data)
    if serializer.is_valid():
        try:
            data = cast(dict[str, Any], serializer.validated_data)
            project = create_project_service(
                name=data["name"],
                workspace_id=data["workspace"].id,
                description=data.get("description", ""),
                deadline=data.get("deadline"),
            )
            response_serializer = ProjectSerializer(project)
            logger.info(
                f"Project created successfully: {project.id} by user: {request.user.id}"
            )
            return success_response(
                data=response_serializer.data,
                message="Project created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Failed to create project - Error: {str(e)}")
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    logger.warning(f"Create project validation failed: {serializer.errors}")
    return validation_error_response(errors=serializer.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def project_detail(request: Request, project_id: int) -> Response:
    logger.debug(
        f"Project detail requested for project_id: {project_id} by user: {request.user.id}"
    )
    try:
        project = get_project_by_id_service(project_id)
        serializer = ProjectDetailSerializer(project)
        logger.info(f"Project detail retrieved successfully: {project_id}")
        return success_response(
            data=serializer.data,
            message="Project retrieved successfully",
        )
    except Exception as e:
        logger.error(
            f"Failed to retrieve project detail for project_id: {project_id} - Error: {str(e)}"
        )
        return error_response(
            message=str(e),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_project(request: Request, project_id: int) -> Response:
    logger.info(
        f"Update project request for project_id: {project_id} by user: {request.user.id}"
    )
    serializer = UpdateProjectSerializer(data=request.data)
    if serializer.is_valid():
        try:
            data = cast(dict[str, Any], serializer.validated_data)
            project = update_project_service(
                project_id=project_id,
                name=data["name"],
                description=data.get("description", ""),
                deadline=data.get("deadline"),
            )
            response_serializer = ProjectSerializer(project)
            logger.info(f"Project updated successfully: {project_id}")
            return success_response(
                data=response_serializer.data,
                message="Project updated successfully",
            )
        except Exception as e:
            logger.error(f"Failed to update project {project_id} - Error: {str(e)}")
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    logger.warning(
        f"Update project validation failed for project_id: {project_id} - Errors: {serializer.errors}"
    )
    return validation_error_response(errors=serializer.errors)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_project(request: Request, project_id: int) -> Response:
    logger.warning(
        f"Delete project request for project_id: {project_id} by user: {request.user.id}"
    )
    try:
        success = delete_project_service(project_id)
        if success:
            logger.info(f"Project deleted successfully: {project_id}")
            return success_response(
                message="Project deleted successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            logger.error(f"Failed to delete project: {project_id}")
            return error_response(
                message="Failed to delete project",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        logger.error(f"Error deleting project {project_id} - Error: {str(e)}")
        return error_response(
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
