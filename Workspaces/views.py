from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def workspace_list(request):
    # Placeholder for fetching workspaces from the database
    pass


@api_view(["POST"])
def create_workspace(request):
    # Placeholder for creating a new workspace
    pass


@api_view(["GET"])
def workspace_detail(request, workspace_id):
    # Placeholder for fetching a specific workspace by ID
    pass


@api_view(["PUT"])
def update_workspace(request, workspace_id):
    # Placeholder for updating a specific workspace by ID
    pass


@api_view(["DELETE"])
def delete_workspace(request, workspace_id):
    # Placeholder for deleting a specific workspace by ID
    pass
