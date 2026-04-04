from django.db import transaction
from rest_framework import serializers

from .models import Bar, Order, OrderItem, Reference, Stock


class ReferenceSerializer(serializers.ModelSerializer):
    """Serializer for Reference model."""

    availability = serializers.SerializerMethodField()

    class Meta:
        model = Reference
        fields = ["id", "ref", "name", "description", "availability"]

    def get_availability(self, obj) -> str:
        """Compute beer availability dynamically."""
        return obj.availability


class BarSerializer(serializers.ModelSerializer):
    """Serializer for Bar model."""

    class Meta:
        model = Bar
        fields = ["id", "name"]


class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model."""

    reference = serializers.StringRelatedField()
    bar = serializers.StringRelatedField()

    class Meta:
        model = Stock
        fields = ["id", "reference", "bar", "quantity"]


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""

    reference = serializers.PrimaryKeyRelatedField(queryset=Reference.objects.all())

    class Meta:
        model = OrderItem
        fields = ["id", "reference", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""

    items = OrderItemSerializer(many=True)
    bar = serializers.PrimaryKeyRelatedField(queryset=Bar.objects.all())

    class Meta:
        model = Order
        fields = ["id", "bar", "created_at", "items"]

    def validate_items(self, value):
        """Ensure stock is available before creating an order."""
        for item in value:
            stock = Stock.objects.filter(
                reference=item["reference"], bar=self.initial_data["bar"]
            ).first()
            if not stock or stock.quantity < item["quantity"]:
                raise serializers.ValidationError(
                    f"Not enough stock for {item['reference'].name}. Available: {stock.quantity if stock else 0}"
                )
        return value

    def create(self, validated_data):
        """Create an order and update stock accordingly."""
        items_data = validated_data.pop("items")

        with transaction.atomic():  # Ensure atomicity
            order = Order.objects.create(**validated_data)
            for item_data in items_data:
                stock = Stock.objects.get(
                    reference=item_data["reference"], bar=validated_data["bar"]
                )
                stock.quantity -= item_data["quantity"]
                stock.save()

                OrderItem.objects.create(order=order, **item_data)

        return order
