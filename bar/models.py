import enum
from typing import Any

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class AvailabilityChoices(enum.Enum):
    """Enum for beer availability status."""

    AVAILABLE = "available"
    OUT_OF_STOCK = "outofstock"


class Reference(models.Model):
    """Model representing a beer reference."""

    ref: str = models.CharField(max_length=50, unique=True)
    name: str = models.CharField(max_length=100)
    description: str = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    @property
    def availability(self) -> str:
        """Determine availability dynamically based on stock."""
        if self.stock_set.filter(quantity__gt=0).exists():
            return AvailabilityChoices.AVAILABLE.value
        return AvailabilityChoices.OUT_OF_STOCK.value


class Bar(models.Model):
    """Model representing a bar counter."""

    name: str = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Stock(models.Model):
    """Model representing the stock of a beer in a specific bar."""

    reference: Reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    bar: Bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    quantity: int = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )

    class Meta:
        unique_together = ("reference", "bar")
        ordering = ["bar", "reference"]

    def __str__(self) -> str:
        return f"{self.reference.name} - {self.bar.name}: {self.quantity} left"


class Order(models.Model):
    """Model representing a customer order."""

    bar: Bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at: Any = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Order {self.id} by {self.user.username} at {self.bar.name}"


class OrderItem(models.Model):
    """Model representing an item in an order."""

    order: Order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    reference: Reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    quantity: int = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("order", "reference")

    def __str__(self) -> str:
        return f"{self.quantity} x {self.reference.name} in Order {self.order.id}"
