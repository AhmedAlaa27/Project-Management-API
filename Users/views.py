from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "User registered successfully",
                "user": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_list(request):
    # Placeholder for fetching users from the database
    pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    # Placeholder for fetching a specific user by ID
    pass


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    # Placeholder for updating a specific user by ID
    pass


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    # Placeholder for deleting a specific user by ID
    pass
