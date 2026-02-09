from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def project_list(request):
    # Placeholder for fetching projects from the database
    pass


@api_view(["POST"])
def create_project(request):
    # Placeholder for creating a new project
    pass


@api_view(["GET"])
def project_detail(request, project_id):
    # Placeholder for fetching a specific project by ID
    pass


@api_view(["PUT"])
def update_project(request, project_id):
    # Placeholder for updating a specific project by ID
    pass


@api_view(["DELETE"])
def delete_project(request, project_id):
    # Placeholder for deleting a specific project by ID
    pass
