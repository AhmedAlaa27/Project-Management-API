import logging
from django.contrib.auth import get_user_model
from django.db import transaction
from typing import Optional

logger = logging.getLogger(__name__)
User = get_user_model()


def list_users_service():
    logger.debug("Fetching all users")
    users = User.objects.all()
    logger.info("Users retrieved successfully")
    return users


def get_user_by_id_service(user_id: int):
    logger.debug(f"Fetching user by id: {user_id}")
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"User found: {user_id}")
        return user
    except User.DoesNotExist:
        logger.error(f"User not found: {user_id}")
        raise


def update_user_service(
    user_id: int, username: Optional[str] = None, email: Optional[str] = None
):
    logger.info(f"Updating user: {user_id}")
    with transaction.atomic():
        try:
            user = User.objects.get(id=user_id)
            if username:
                logger.debug(f"Updating username for user {user_id}: {username}")
                user.username = username
            if email:
                logger.debug(f"Updating email for user {user_id}: {email}")
                user.email = email
            user.save()
            logger.info(f"User updated successfully: {user_id}")
            return user
        except User.DoesNotExist:
            logger.error(f"Cannot update - User not found: {user_id}")
            raise
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise


def delete_user_service(user_id: int) -> bool:
    logger.warning(f"Deleting user: {user_id}")
    with transaction.atomic():
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            logger.info(f"User deleted successfully: {user_id}")
            return True
        except User.DoesNotExist:
            logger.error(f"Cannot delete - User not found: {user_id}")
            raise
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise
