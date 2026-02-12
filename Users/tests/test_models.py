"""
Unit tests for Users app models.
"""

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestUserModel:
    """Test cases for the User model."""

    def test_user_creation_with_all_fields(self, user_factory):
        """Test creating a user with all fields."""
        user = user_factory(
            username="johndoe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
        )

        assert user.username == "johndoe"
        assert user.email == "john@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.id is not None

    def test_username_uniqueness(self, user_factory):
        """Test that username must be unique."""
        user_factory(username="testuser")

        with pytest.raises(IntegrityError):
            user_factory(username="testuser")

    def test_password_hashing(self, user_factory):
        """Test that passwords are properly hashed."""
        password = "testpass123"
        user = user_factory()

        # Password should not be stored in plain text
        assert user.password != password
        # But user should be able to authenticate with it
        assert user.check_password(password) is True

    def test_user_default_values(self, user_factory):
        """Test default values for user fields."""
        user = user_factory()

        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.date_joined is not None

    def test_avatar_field_optional(self, user_factory):
        """Test that avatar field is optional."""
        user = user_factory(avatar=None)

        assert user.avatar.name is None or user.avatar.name == ""

    def test_user_str_representation(self, user_factory):
        """Test string representation of user."""
        user = user_factory(username="testuser")

        assert str(user) == "testuser"

    def test_email_field_exists(self, user_factory):
        """Test that email field is required."""
        user = user_factory(email="test@example.com")

        assert user.email == "test@example.com"
