from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.register, name="register"),
    path("", views.user_list, name="user-list"),
    path("<int:user_id>/", views.user_detail, name="user-detail"),
    path("<int:user_id>/update/", views.update_user, name="user-update"),
    path("<int:user_id>/delete/", views.delete_user, name="user-delete"),
]
