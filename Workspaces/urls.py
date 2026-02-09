from django.urls import path
from . import views

urlpatterns = [
    path("", views.workspace_list, name="workspace_list"),
    path("me/", views.user_workspace_list, name="user_workspace_list"),
    path("create/", views.create_workspace, name="create_workspace"),
    path("<int:workspace_id>/", views.workspace_detail, name="workspace_detail"),
    path("<int:workspace_id>/update/", views.update_workspace, name="update_workspace"),
    path("<int:workspace_id>/delete/", views.delete_workspace, name="delete_workspace"),
]
