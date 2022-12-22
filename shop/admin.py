from django.contrib import admin

from .models import Product, Order, OrderItem, ProductImage, Size, ProductReview


class OrderItemInline(admin.TabularInline):
    extra = 0
    model = OrderItem
    fk_name = 'cart'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['refund_code', 'user', 'completed']
    list_filter = ('completed', )
    inlines = [OrderItemInline, ]


class ProductPhotoAdmin(admin.TabularInline):
    extra = 0
    model = ProductImage
    fk_name = 'item'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price']
    inlines = [ProductPhotoAdmin,]


admin.site.register(OrderItem)
admin.site.register(Size)
admin.site.register(ProductReview)
