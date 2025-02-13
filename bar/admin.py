from django.contrib import admin


from .models import Bar, Order, OrderItem, Reference, Stock


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("name", "ref", "availability")
    search_fields = ("name", "ref")


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("reference", "bar", "quantity")
    list_filter = ("bar",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "bar", "user", "created_at")
    list_filter = ("bar", "created_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "reference", "quantity")
