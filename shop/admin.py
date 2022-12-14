from django.contrib import admin

from .models import Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    extra = 0
    model = Order.items.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['ref_code', 'user', 'completed']
    list_filter = ('completed', )
    inlines = [OrderItemInline, ]


@admin.register(Product)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price']


admin.site.register(OrderItem)