import pytest
from rest_framework import status

from bar.models import Order, Stock


@pytest.mark.django_db
def test_create_order(
    api_client, create_user, create_bar, create_reference, create_stock
):
    """Test that a client can successfully create an order."""
    api_client.force_authenticate(user=create_user)

    payload = {
        "bar": create_bar.id,
        "items": [{"reference": create_reference.id, "quantity": 2}],
    }

    response = api_client.post("/api/bar/orders/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == 1
    assert (
        Stock.objects.get(reference=create_reference, bar=create_bar).quantity == 6
    )  # Stock updated correctly
