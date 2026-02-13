import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import Any, cast

logger = logging.getLogger(__name__)

from Users.serializers import RegisterSerializer, UpdateUserSerializer, UserSerializer
from Users.services import (
    delete_user_service,
    get_user_by_id_service,
    list_users_service,
    update_user_service,
)
from utils.responses import success_response, error_response, validation_error_response


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request: Request) -> Response:
    logger.info(
        f"User registration attempt with username: {request.data.get('username')}"
    )
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"User registered successfully: {serializer.data.get('username')}")
        return success_response(
            data=serializer.data,
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED,
        )
    logger.warning(f"User registration failed: {serializer.errors}")
    return validation_error_response(errors=serializer.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_list(request: Request) -> Response:
    logger.debug(f"User list requested by user: {request.user.id}")
    users = list_users_service()
    serializer = UserSerializer(users, many=True)
    logger.info(f"Retrieved {len(users)} users")
    return success_response(
        data=serializer.data,
        message="Users retrieved successfully",
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_detail(request: Request, user_id: int) -> Response:
    logger.debug(
        f"User detail requested for user_id: {user_id} by user: {request.user.id}"
    )
    try:
        user = get_user_by_id_service(user_id)
        serializer = UserSerializer(user)
        logger.info(f"User detail retrieved successfully for user_id: {user_id}")
        return success_response(
            data=serializer.data,
            message="User retrieved successfully",
        )
    except Exception as e:
        logger.error(
            f"Failed to retrieve user detail for user_id: {user_id} - Error: {str(e)}"
        )
        return error_response(
            message=str(e),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request: Request, user_id: int) -> Response:
    logger.info(
        f"Update user request for user_id: {user_id} by user: {request.user.id}"
    )
    serializer = UpdateUserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            data = cast(dict[str, Any], serializer.validated_data)
            user = update_user_service(
                user_id=user_id,
                username=data.get("username"),
                email=data.get("email"),
            )
            response_serializer = UserSerializer(user)
            logger.info(f"User updated successfully: user_id={user_id}")
            return success_response(
                data=response_serializer.data,
                message="User updated successfully",
            )
        except Exception as e:
            logger.error(f"Failed to update user {user_id} - Error: {str(e)}")
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    logger.warning(
        f"Update user validation failed for user_id: {user_id} - Errors: {serializer.errors}"
    )
    return validation_error_response(errors=serializer.errors)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request: Request, user_id: int) -> Response:
    logger.warning(
        f"Delete user request for user_id: {user_id} by user: {request.user.id}"
    )
    try:
        success = delete_user_service(user_id)
        if success:
            logger.info(f"User deleted successfully: user_id={user_id}")
            return success_response(
                message="User deleted successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            logger.error(f"Failed to delete user: user_id={user_id}")
            return error_response(
                message="Failed to delete user",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        logger.error(f"Error deleting user {user_id} - Error: {str(e)}")
        return error_response(
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
