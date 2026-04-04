import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OrderItem, Stock

logger = logging.getLogger("low_stock_logger")


@receiver(post_save, sender=OrderItem)
def update_stock_on_order(sender, instance, **kwargs):
    """Reduce stock when an order is placed and log warnings for low stock."""
    stock = Stock.objects.filter(
        reference=instance.reference, bar=instance.order.bar
    ).first()
    if stock:
        stock.quantity -= instance.quantity
        stock.save()

        if stock.quantity < 2:
            logger.warning(
                f"Low stock alert: {stock.reference.name} at {stock.bar.name}. Remaining: {stock.quantity}"
            )
