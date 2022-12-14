from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.shortcuts import get_object_or_404

from shop.models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class OrderView(RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'uuid'

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        obj = get_object_or_404(Order, UUID=uuid)
        return obj

