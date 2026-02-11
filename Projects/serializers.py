from rest_framework import serializers

from Projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "workspace",
            "deadline",
            "created_at",
            "updated_at",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer for project detail view with nested tasks"""

    from Tasks.serializers import TaskSerializer

    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "workspace",
            "deadline",
            "created_at",
            "updated_at",
            "tasks",
        ]


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description", "workspace", "deadline"]


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "description", "deadline"]
