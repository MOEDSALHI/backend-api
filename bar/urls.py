from django.urls import include, path
from rest_framework.routers import SimpleRouter

from bar.views import BarViewSet, OrderViewSet, ReferenceViewSet, StockViewSet

# Creating the router for ViewSets
router = SimpleRouter()
router.register(r"references", ReferenceViewSet, basename="reference")
router.register(r"bars", BarViewSet, basename="bar")
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
