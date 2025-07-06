import pytest
from django.utils.timezone import now, timedelta
from django.urls import reverse
from interview.inventory.models import Inventory, InventoryLanguage, InventoryType


@pytest.mark.django_db
def test_inventory_filter_created_after(client):
    language = InventoryLanguage.objects.create(name="English")
    inv_type = InventoryType.objects.create(name="Default Type")

    Inventory.objects.create(
        name="Old Inventory Item",
        metadata={},
        language=language,
        type=inv_type
    )

    Inventory.objects.create(
        name="New Inventory Item",
        metadata={},
        language=language,
        type=inv_type
    )

    # First: filter everything created after 3 days ago (should include New)
    filter_date = (now() - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = reverse("inventory-list") + f"?created_after={filter_date}"

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    names = [item["name"] for item in data["results"]]
    assert "Old Inventory Item" in names
    assert "New Inventory Item" in names


    # Second: filter after a future timestamp (should return nothing)
    filter_date = (now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = reverse("inventory-list") + f"?created_after={filter_date}"
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data["results"]) == 0


@pytest.mark.django_db
def test_inventory_list_create_pagination(client):
    language = InventoryLanguage.objects.create(name="English")
    inv_type = InventoryType.objects.create(name="Default Type")

    # Create 5 inventory items with different created_at dates
    Inventory.objects.create(
        name="Old Inventory Item 1",
        metadata={},
        language=language,
        type=inv_type,
        created_at=now() - timedelta(days=10)
    )
    Inventory.objects.create(
        name="Old Inventory Item 2",
        metadata={},
        language=language,
        type=inv_type,
        created_at=now() - timedelta(days=5)
    )
    Inventory.objects.create(
        name="New Inventory Item 1",
        metadata={},
        language=language,
        type=inv_type,
        created_at=now() - timedelta(days=2)
    )
    Inventory.objects.create(
        name="New Inventory Item 2",
        metadata={},
        language=language,
        type=inv_type,
        created_at=now() - timedelta(days=1)
    )
    Inventory.objects.create(
        name="Newest Inventory Item",
        metadata={},
        language=language,
        type=inv_type,
        created_at=now()
    )

    url = reverse("inventory-list")

    # Test default pagination: limit=3, offset=0
    response = client.get(url + "?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 5
    assert len(data["results"]) == 3
    assert data["next"] is not None
    assert data["previous"] is None

    # Test pagination with offset=3, limit=3 (should return remaining 2 items)
    response = client.get(url + "?limit=3&offset=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2
    assert data["previous"] is not None
