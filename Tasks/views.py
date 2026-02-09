from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def task_list(request):
    # Placeholder for fetching tasks from the database
    pass


@api_view(["POST"])
def create_task(request):
    # Placeholder for creating a new task
    pass


@api_view(["GET"])
def task_detail(request, task_id):
    # Placeholder for fetching a specific task by ID
    pass


@api_view(["PUT"])
def update_task(request, task_id):
    # Placeholder for updating a specific task by ID
    pass


@api_view(["DELETE"])
def delete_task(request, task_id):
    # Placeholder for deleting a specific task by ID
    pass
