from rest_framework import serializers

from shop.models import Product, Order, OrderItem, ProductImage, ProductReview, Size


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            'title',
            "price",
            "slug",
            "image",
            "color",
            "get_overall_rating",
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'file',
        )


class ProductReviewSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = ProductReview
        fields = (
            'user',
            'rating',
            'comment'
        )


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = (
            'value',
        )


class ProductDetailSerializer(serializers.ModelSerializer):

    photos = ProductImageSerializer(read_only=True, many=True)
    reviews = ProductReviewSerializer(read_only=True, many=True)
    size = ProductSizeSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            'title',
            "price",
            "slug",
            "image",
            "color",
            "photos",
            "reviews",
            "size",
            "get_overall_rating",
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
            "refund_code",
            "total_items",
            "total_price",
        )
        read_only_fields = ('total_items', 'total_price', 'order_items')

    def get_order_items(self, obj):
        items = obj.items.all()
        if items.exists():
            return OrderItemSerializer(items, many=True).data
        return []

    def get_total_items(self, obj):
        return obj.get_total_items()

    def get_total_price(self, obj):
        return obj.get_total_price()

