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

    names = [item["name"] for item in data]
    assert "Old Inventory Item" in names
    assert "New Inventory Item" in names


    # Second: filter after a future timestamp (should return nothing)
    filter_date = (now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = reverse("inventory-list") + f"?created_after={filter_date}"
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 0
