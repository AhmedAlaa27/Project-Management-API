"""
Unit tests for Users app serializers.
"""

import pytest
from django.contrib.auth import get_user_model
from Users.serializers import (
    RegisterSerializer,
    UpdateUserSerializer,
    UserSerializer,
)

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.unit
class TestRegisterSerializer:
    """Test cases for RegisterSerializer."""

    def test_serializer_with_valid_data(self):
        """Test serializer with valid registration data."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpass123",
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data["username"] == "newuser"
        assert serializer.validated_data["email"] == "newuser@example.com"

    def test_password_is_write_only(self):
        """Test that password field is write-only."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }
        serializer = RegisterSerializer(data=data)
        serializer.is_valid()
        user = serializer.save()

        # Password should not appear in serialized output
        serialized_data = RegisterSerializer(user).data
        assert "password" not in serialized_data

    def test_create_method_hashes_password(self):
        """Test that create method properly hashes password."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "plainpassword",
        }
        serializer = RegisterSerializer(data=data)
        serializer.is_valid()
        user = serializer.save()

        # Password should be hashed
        assert user.password != "plainpassword"
        assert user.check_password("plainpassword") is True

    def test_missing_required_fields(self):
        """Test validation fails with missing required fields."""
        data = {"username": "testuser"}
        serializer = RegisterSerializer(data=data)

        assert not serializer.is_valid()
        # Password is required, but email is optional in Django's default User model
        assert "password" in serializer.errors

    def test_avatar_field_optional(self):
        """Test that avatar field is optional."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid()


@pytest.mark.unit
class TestUpdateUserSerializer:
    """Test cases for UpdateUserSerializer."""

    def test_update_username_and_email(self, user_factory):
        """Test updating user's username and email."""
        user = user_factory(username="oldusername", email="old@example.com")
        data = {
            "username": "newusername",
            "email": "new@example.com",
        }
        serializer = UpdateUserSerializer(user, data=data, partial=True)

        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.username == "newusername"
        assert updated_user.email == "new@example.com"

    def test_partial_update(self, user_factory):
        """Test partial update of user fields."""
        user = user_factory(username="testuser", email="test@example.com")
        data = {"username": "updateduser"}
        serializer = UpdateUserSerializer(user, data=data, partial=True)

        assert serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.username == "updateduser"
        assert updated_user.email == "test@example.com"  # Should remain unchanged


@pytest.mark.unit
class TestUserSerializer:
    """Test cases for UserSerializer (read-only)."""

    def test_serializer_output(self, user_factory):
        """Test serializer output contains correct fields."""
        user = user_factory(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        serializer = UserSerializer(user)

        assert "id" in serializer.data
        assert serializer.data["username"] == "testuser"
        assert serializer.data["email"] == "test@example.com"
        assert serializer.data["first_name"] == "Test"
        assert serializer.data["last_name"] == "User"
        assert "date_joined" in serializer.data

    def test_password_not_in_output(self, user_factory):
        """Test that password is not exposed in serializer output."""
        user = user_factory()
        serializer = UserSerializer(user)

        assert "password" not in serializer.data
