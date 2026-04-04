from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.permissions import IsStaffOrReadOnly

from .models import Bar, Order, Reference, Stock
from .serializers import (
    BarSerializer,
    OrderSerializer,
    ReferenceSerializer,
    StockSerializer,
)


class ReferenceViewSet(viewsets.ModelViewSet):
    """API endpoint for managing beer references."""

    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "ref"]
    ordering_fields = ["name"]


class BarViewSet(viewsets.ModelViewSet):
    """API endpoint for managing bars."""

    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing stock (Read-Only)."""

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["bar", "reference"]
    ordering_fields = ["quantity"]


class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint for managing orders."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at"]

    def perform_create(self, serializer):
        """Ensure only authenticated users can create an order."""
        serializer.validated_data["user"] = self.request.user
        serializer.save()

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def stock_status(self, request, pk=None):
        """Check stock levels for an order."""
        order = self.get_object()
        stock_status = [
            {
                "reference": item.reference.name,
                "ordered_quantity": item.quantity,
                "remaining_stock": Stock.objects.get(
                    reference=item.reference, bar=order.bar
                ).quantity,
            }
            for item in order.items.all()
        ]
        return Response(stock_status, status=status.HTTP_200_OK)
