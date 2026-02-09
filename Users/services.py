from django.contrib.auth import get_user_model
from django.db import transaction
from typing import Optional

User = get_user_model()


def list_users_service():
    return User.objects.all()


def get_user_by_id_service(user_id: int):
    return User.objects.get(id=user_id)


def update_user_service(
    user_id: int, username: Optional[str] = None, email: Optional[str] = None
):
    with transaction.atomic():
        user = User.objects.get(id=user_id)
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()
        return user


def delete_user_service(user_id: int) -> bool:
    with transaction.atomic():
        user = User.objects.get(id=user_id)
        user.delete()
        return True
