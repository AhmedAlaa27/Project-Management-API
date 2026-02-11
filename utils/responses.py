from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional, Union


def success_response(
    data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK
) -> Response:
    """
    Standard success response wrapper.

    Args:
        data: The response data (can be None for DELETE operations)
        message: Success message
        status_code: HTTP status code (default: 200)

    Returns:
        Response object with standardized format
    """
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
            "errors": None,
        },
        status=status_code,
    )


def error_response(
    message: str = "An error occurred",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    errors: Optional[dict] = None,
) -> Response:
    """
    Standard error response wrapper.

    Args:
        message: Error message
        status_code: HTTP status code (default: 400)
        errors: Optional field-specific errors dictionary

    Returns:
        Response object with standardized format
    """
    return Response(
        {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors,
        },
        status=status_code,
    )


def validation_error_response(
    errors: Union[dict, Any],
    message: str = "Validation failed",
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Standard validation error response wrapper.

    Args:
        errors: Dictionary of field-specific validation errors (from serializer.errors)
        status_code: HTTP status code (default: 400)

    Returns:
        Response object with standardized format
    """
    return Response(
        {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors,
        },
        status=status_code,
    )
