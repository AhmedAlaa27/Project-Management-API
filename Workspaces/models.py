from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Workspace(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="owned_workspaces"
    )
    members = models.ManyToManyField(get_user_model(), related_name="workspaces")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workspaces"

    def __str__(self):
        return f"{self.name} | {self.owner.username}"
