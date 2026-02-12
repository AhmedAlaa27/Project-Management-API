"""
Integration tests for Users app API endpoints.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.integration
class TestRegisterAPI:
    """Test cases for user registration endpoint."""

    def test_register_user_success(self, api_client):
        """Test successful user registration."""
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpass123",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["message"] == "User registered successfully"
        assert "username" in response.data["data"]
        assert response.data["data"]["username"] == "newuser"
        # Verify user was created in database
        assert User.objects.filter(username="newuser").exists()

    def test_register_duplicate_username(self, api_client, user_factory):
        """Test registration fails with duplicate username."""
        user_factory(username="existinguser")
        url = reverse("register")
        data = {
            "username": "existinguser",
            "email": "new@example.com",
            "password": "testpass123",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False

    def test_register_missing_required_fields(self, api_client):
        """Test registration fails with missing required fields."""
        url = reverse("register")
        data = {"username": "testuser"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert "errors" in response.data

    def test_register_no_authentication_required(self, api_client):
        """Test that registration doesn't require authentication."""
        url = reverse("register")
        data = {
            "username": "publicuser",
            "email": "public@example.com",
            "password": "testpass123",
        }

        # Should work without authentication
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.integration
class TestJWTTokenAPI:
    """Test cases for JWT token endpoints."""

    def test_obtain_token_with_valid_credentials(self, api_client, user_factory):
        """Test obtaining JWT token with valid credentials."""
        user = user_factory(username="testuser")
        url = reverse("token_obtain_pair")
        data = {
            "username": "testuser",
            "password": "testpass123",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_obtain_token_with_invalid_credentials(self, api_client):
        """Test token generation fails with invalid credentials."""
        url = reverse("token_obtain_pair")
        data = {
            "username": "nonexistent",
            "password": "wrongpass",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token(self, api_client, get_tokens_for_user, user_factory):
        """Test refreshing access token."""
        user = user_factory()
        tokens = get_tokens_for_user(user)
        url = reverse("token_refresh")
        data = {"refresh": tokens["refresh"]}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data


@pytest.mark.integration
class TestUserListAPI:
    """Test cases for listing users."""

    def test_list_users_authenticated(self, authenticated_client, user_factory):
        """Test listing users with authentication."""
        user_factory.create_batch(3)
        url = reverse("user-list")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["data"]) >= 3

    def test_list_users_unauthenticated(self, api_client):
        """Test listing users fails without authentication."""
        url = reverse("user-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestUserDetailAPI:
    """Test cases for user detail endpoint."""

    def test_get_user_detail_authenticated(self, authenticated_client, user_factory):
        """Test getting user details with authentication."""
        user = user_factory(username="detailuser")
        url = reverse("user-detail", kwargs={"user_id": user.id})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["username"] == "detailuser"

    def test_get_user_detail_unauthenticated(self, api_client, user_factory):
        """Test getting user details fails without authentication."""
        user = user_factory()
        url = reverse("user-detail", kwargs={"user_id": user.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_nonexistent_user(self, authenticated_client):
        """Test getting details of nonexistent user."""
        url = reverse("user-detail", kwargs={"user_id": 9999})

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["success"] is False


@pytest.mark.integration
class TestUpdateUserAPI:
    """Test cases for updating user."""

    def test_update_user_authenticated(self, authenticated_client, user_factory):
        """Test updating user with authentication."""
        user = user_factory(username="oldname", email="old@example.com")
        url = reverse("user-update", kwargs={"user_id": user.id})
        data = {
            "username": "newname",
            "email": "new@example.com",
        }

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["username"] == "newname"
        assert response.data["data"]["email"] == "new@example.com"

    def test_update_user_partial(self, authenticated_client, user_factory):
        """Test partial update of user."""
        user = user_factory(username="partialuser", email="test@example.com")
        url = reverse("user-update", kwargs={"user_id": user.id})
        data = {"username": "updatedname"}

        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["username"] == "updatedname"

    def test_update_user_unauthenticated(self, api_client, user_factory):
        """Test updating user fails without authentication."""
        user = user_factory()
        url = reverse("user-update", kwargs={"user_id": user.id})
        data = {"username": "newname"}

        response = api_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestDeleteUserAPI:
    """Test cases for deleting user."""

    def test_delete_user_authenticated(self, authenticated_client, user_factory):
        """Test deleting user with authentication."""
        user = user_factory()
        url = reverse("user-delete", kwargs={"user_id": user.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert not User.objects.filter(id=user.id).exists()

    def test_delete_user_unauthenticated(self, api_client, user_factory):
        """Test deleting user fails without authentication."""
        user = user_factory()
        url = reverse("user-delete", kwargs={"user_id": user.id})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_nonexistent_user(self, authenticated_client):
        """Test deleting nonexistent user."""
        url = reverse("user-delete", kwargs={"user_id": 9999})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
