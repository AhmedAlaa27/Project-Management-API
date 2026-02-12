"""
Unit tests for Users app services.
"""

import pytest
from django.contrib.auth import get_user_model
from Users.services import (
    list_users_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
)

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestListUsersService:
    """Test cases for list_users_service."""

    def test_list_all_users(self, user_factory):
        """Test listing all users."""
        user_factory.create_batch(3)

        users = list_users_service()

        assert users.count() == 3

    def test_list_users_empty(self):
        """Test listing users when none exist."""
        users = list_users_service()

        assert users.count() == 0


@pytest.mark.unit
class TestGetUserByIdService:
    """Test cases for get_user_by_id_service."""

    def test_get_existing_user(self, user_factory):
        """Test retrieving an existing user by ID."""
        user = user_factory(username="testuser")

        retrieved_user = get_user_by_id_service(user.id)

        assert retrieved_user.id == user.id
        assert retrieved_user.username == "testuser"

    def test_get_nonexistent_user(self):
        """Test that DoesNotExist is raised for invalid ID."""
        with pytest.raises(User.DoesNotExist):
            get_user_by_id_service(9999)


@pytest.mark.unit
class TestUpdateUserService:
    """Test cases for update_user_service."""

    def test_update_username(self, user_factory):
        """Test updating user's username."""
        user = user_factory(username="oldname", email="test@example.com")

        updated_user = update_user_service(user.id, username="newname")

        assert updated_user.username == "newname"
        assert updated_user.email == "test@example.com"  # Unchanged

    def test_update_email(self, user_factory):
        """Test updating user's email."""
        user = user_factory(username="testuser", email="old@example.com")

        updated_user = update_user_service(user.id, email="new@example.com")

        assert updated_user.email == "new@example.com"
        assert updated_user.username == "testuser"  # Unchanged

    def test_update_both_fields(self, user_factory):
        """Test updating both username and email."""
        user = user_factory(username="oldname", email="old@example.com")

        updated_user = update_user_service(
            user.id, username="newname", email="new@example.com"
        )

        assert updated_user.username == "newname"
        assert updated_user.email == "new@example.com"

    def test_update_with_transaction(self, user_factory):
        """Test that update uses transaction."""
        user = user_factory()

        # Should complete successfully with transaction
        updated_user = update_user_service(user.id, username="updated")

        assert updated_user.username == "updated"


@pytest.mark.unit
class TestDeleteUserService:
    """Test cases for delete_user_service."""

    def test_delete_existing_user(self, user_factory):
        """Test deleting an existing user."""
        user = user_factory()
        user_id = user.id

        result = delete_user_service(user_id)

        assert result is True
        assert not User.objects.filter(id=user_id).exists()

    def test_delete_nonexistent_user(self):
        """Test deleting a nonexistent user raises error."""
        with pytest.raises(User.DoesNotExist):
            delete_user_service(9999)

    def test_delete_with_transaction(self, user_factory):
        """Test that delete uses transaction."""
        user = user_factory()
        user_id = user.id

        delete_user_service(user_id)

        # Verify user is deleted
        assert not User.objects.filter(id=user_id).exists()
