"""
Root conftest.py to make fixtures available to all test directories.

This file imports and re-exports all fixtures and factory registrations
from tests/conftest.py to make them available throughout the project.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from pytest_factoryboy import register

from tests.factories import (
    UserFactory,
    WorkspaceFactory,
    ProjectFactory,
    TaskFactory,
)

# Register all factories for pytest-factoryboy
register(UserFactory)
register(WorkspaceFactory)
register(ProjectFactory)
register(TaskFactory)


@pytest.fixture
def api_client():
    """Provide an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def test_password():
    """Provide a consistent test password."""
    return "testpass123"


@pytest.fixture
def create_user(db, user_factory):
    """Factory to create a user with a known password."""

    def make_user(**kwargs):
        return user_factory(**kwargs)

    return make_user


@pytest.fixture
def authenticated_user(db, user_factory):
    """Create an authenticated test user."""
    return user_factory(username="testuser", email="testuser@example.com")


@pytest.fixture
def authenticated_client(authenticated_user):
    """Provide an authenticated API client with JWT token."""
    client = APIClient()
    refresh = RefreshToken.for_user(authenticated_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def another_user(db, user_factory):
    """Create another user for testing multi-user scenarios."""
    return user_factory(username="anotheruser", email="anotheruser@example.com")


@pytest.fixture
def get_tokens_for_user():
    """Helper to generate JWT tokens for any user."""

    def _get_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    return _get_tokens
