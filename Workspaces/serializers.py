from rest_framework import serializers

from Workspaces.models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["id", "name", "description", "created_at"]


class WorkspaceDetailSerializer(serializers.ModelSerializer):
    """Serializer for workspace detail view with nested projects"""

    from Projects.serializers import ProjectSerializer

    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Workspace
        fields = ["id", "name", "description", "created_at", "projects"]


class UpdateWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ["name", "description"]
