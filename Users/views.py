from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from typing import Any, cast

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
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return success_response(
            data=serializer.data,
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED,
        )
    return validation_error_response(errors=serializer.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_list(request: Request) -> Response:
    users = list_users_service()
    serializer = UserSerializer(users, many=True)
    return success_response(
        data=serializer.data,
        message="Users retrieved successfully",
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_detail(request: Request, user_id: int) -> Response:
    try:
        user = get_user_by_id_service(user_id)
        serializer = UserSerializer(user)
        return success_response(
            data=serializer.data,
            message="User retrieved successfully",
        )
    except Exception as e:
        return error_response(
            message=str(e),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request: Request, user_id: int) -> Response:
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
            return success_response(
                data=response_serializer.data,
                message="User updated successfully",
            )
        except Exception as e:
            return error_response(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    return validation_error_response(errors=serializer.errors)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request: Request, user_id: int) -> Response:
    try:
        success = delete_user_service(user_id)
        if success:
            return success_response(
                message="User deleted successfully",
                status_code=status.HTTP_200_OK,
            )
        else:
            return error_response(
                message="Failed to delete user",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return error_response(
            message=str(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
