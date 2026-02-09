from rest_framework import serializers

from Tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "project",
            "assignees",
            "author",
            "status",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
        ]


class CreateTaskSerializer(serializers.ModelSerializer):
    assignee_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "project",
            "status",
            "priority",
            "due_date",
            "assignee_ids",
        ]


class UpdateTaskSerializer(serializers.ModelSerializer):
    assignee_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "priority",
            "due_date",
            "assignee_ids",
        ]
