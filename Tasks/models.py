from django.db import models
from django.contrib.auth import get_user_model

from Projects.models import Project


# Create your models here.
class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "L", "Low"
        MEDIUM = "M", "Medium"
        HIGH = "H", "High"

    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(get_user_model(), related_name="tasks")
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="authored_tasks",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.TODO
    )
    priority = models.CharField(
        max_length=50, choices=Priority.choices, default=Priority.MEDIUM
    )
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.project.name} | {self.project.workspace.name} | {self.author.username if self.author else 'No Author'}"
