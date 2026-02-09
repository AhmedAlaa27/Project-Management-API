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
    path("", views.user_list, name="user_list"),
    path("<int:user_id>/", views.user_detail, name="user_detail"),
    path("<int:user_id>/update/", views.update_user, name="update_user"),
    path("<int:user_id>/delete/", views.delete_user, name="delete_user"),
]
