import pytest
from rest_framework import status

from bar.models import Reference


@pytest.mark.django_db
def test_get_references(api_client, create_reference):
    """Test retrieving beer references."""
    response = api_client.get("/api/bar/references/")
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]
    assert len(results) == 1
    assert results[0]["name"] == "Leffe Blonde"
