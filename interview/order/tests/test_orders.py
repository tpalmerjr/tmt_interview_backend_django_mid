import pytest
from django.urls import reverse
from django.utils.timezone import now, timedelta

from interview.inventory.models import Inventory, InventoryType, InventoryLanguage
from interview.order.models import Order, OrderTag


@pytest.mark.django_db
def test_deactivate_order(client):
    # Set up required related models
    language = InventoryLanguage.objects.create(name="English")
    inv_type = InventoryType.objects.create(name="Video")
    inventory = Inventory.objects.create(
        name="Test Inventory",
        metadata={},
        language=language,
        type=inv_type,
    )

    # Set up order and tag
    tag = OrderTag.objects.create(name="Urgent")
    order = Order.objects.create(
        inventory=inventory,
        start_date=now().date(),
        embargo_date=(now() + timedelta(days=1)).date(),
        is_active=True,
    )
    order.tags.add(tag)

    # Verify order is active before the call
    assert order.is_active is True

    # Call the deactivate endpoint
    url = reverse("order-deactivate", kwargs={"pk": order.id})
    response = client.patch(url)  # using patch but could be done with POST

    assert response.status_code == 200
    order.refresh_from_db()
    assert order.is_active is False
