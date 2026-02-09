from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_list(request):
    # Placeholder for fetching tasks from the database
    pass


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):
    # Placeholder for creating a new task
    pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id):
    # Placeholder for fetching a specific task by ID
    pass


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    # Placeholder for updating a specific task by ID
    pass


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    # Placeholder for deleting a specific task by ID
    pass
