from rest_framework import serializers

from shop.models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title',
            "description",
            "price",
            "slug",
        )


class OrderItemSerializer(serializers.ModelSerializer):

    item = serializers.StringRelatedField()
    total_price = serializers.SerializerMethodField()
    item_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            "item",
            "quantity",
            "item_price",
            "total_price",
        )

    def get_total_price(self, obj):
        return obj.get_total_price()

    def get_item_price(self, obj):
        return obj.item.price


class OrderSerializer(serializers.ModelSerializer):

    total_items = serializers.SerializerMethodField()
    order_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = (
            "UUID",
            "user",
            "order_items",
            "completed",
            "ref_code",
            "total_items",
            "total_price",
        )
        read_only_fields = ('total_items', 'total_price', 'order_items')

    def get_order_items(self, obj):
        item = OrderItem.objects.filter(order=obj, completed=False, user=obj.user)
        if item.exists():
            return OrderItemSerializer(obj.items.filter(user=obj.user, completed=False), many=True).data
        return []

    def get_total_items(self, obj):
        return obj.get_total_items()

    def get_total_price(self, obj):
        return obj.get_total_price()

