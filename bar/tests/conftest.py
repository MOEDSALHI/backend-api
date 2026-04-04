import pytest
from django.contrib.auth.models import Group, User
from rest_framework.test import APIClient

from bar.models import Bar, Reference, Stock


@pytest.fixture
def api_client():
    """Fixture to create a DRF APIClient instance."""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Fixture to create a regular user (client)."""
    user = User.objects.create_user(username="client", password="testpassword")
    group, _ = Group.objects.get_or_create(name="Clients")
    user.groups.add(group)
    return user


@pytest.fixture
def create_staff_user(db):
    """Fixture to create a staff user."""
    user = User.objects.create_user(
        username="staff", password="staffpassword", is_staff=True
    )
    group, _ = Group.objects.get_or_create(name="Staff")
    user.groups.add(group)
    return user


@pytest.fixture
def create_reference(db):
    """Fixture to create a beer reference."""
    return Reference.objects.create(
        ref="leffeblonde", name="Leffe Blonde", description="Belgian Abbey Beer."
    )


@pytest.fixture
def create_bar(db):
    """Fixture to create a bar."""
    return Bar.objects.create(name="First Floor")


@pytest.fixture
def create_stock(db, create_reference, create_bar):
    """Fixture to create stock for a reference in a bar."""
    return Stock.objects.create(reference=create_reference, bar=create_bar, quantity=10)
