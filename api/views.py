from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from shop.models import Product, Order, OrderItem
from .serializers import ProductSerializer, ProductDetailSerializer, OrderSerializer

"""
TODO: 
- pagination
- authentication
- permissions
- ShippingAddress model
- Checkout view
- Payment
- payment view
- order completing processes (changes in particular fields with signals)
"""


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'


class OrderView(RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'uuid'

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        obj = get_object_or_404(Order, UUID=uuid)
        return obj


class AddToCart(APIView):
    def post(self, request, slug, format=None):
        order = Order.objects.filter(user=request.user, completed=False)
        product = get_object_or_404(Product, slug=slug)

        if order.exists():
            current_order = order.last()
            item = OrderItem.objects.filter(order=current_order, item=product, completed=False, user=request.user)
            order_serializer = OrderSerializer(order, many=False)

            if item.exists():
                item = item.first()
                item.quantity += 1
                item.save()

                # return Response(order_serializer.data, status=status.HTTP_200_OK)
                return Response({"message": f"{item.item.title} quantity increased"}, status=status.HTTP_200_OK)

            else:

                user_orderitem = OrderItem.objects.create(
                    user=request.user,
                    item=product,
                    quantity=1,
                )
                current_order.items.add(user_orderitem)

                # return Response(order_serializer.data, status=status.HTTP_200_OK)
                return Response({"message": f"{user_orderitem.item.title} added to the cart"}, status=status.HTTP_200_OK)

        else:
            user_order = Order.objects.create(
                user=request.user,
                completed=False,
            )

            user_orderitem = OrderItem.objects.create(
                user=request.user,
                completed=False,
                item=product,
                quantity=1
            )

            user_order.items.add(user_orderitem)

            order_serializer = OrderSerializer(user_order)

            # return Response(order_serializer.data, status=status.HTTP_200_OK)
            return Response({"message": f"{user_orderitem.item.title} added to your cart"}, status=status.HTTP_200_OK)


class RemoveAllFromCart(APIView):

    def post(self, request, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        order = Order.objects.filter(user=self.request.user).first()
        item = OrderItem.objects.filter(order=order, item=product, user=self.request.user, completed=False)

        if item.exists():
            item = item[0]
            item.delete()
            return Response({"message": f"{item.item.title} completely removed from the cart"})

        return Response({"message": f"No item in the cart"}, status=status.HTTP_404_NOT_FOUND)


class RemoveSingleFromCart(APIView):
    def post(self, request, slug, format=None):
        product = get_object_or_404(Product, slug=slug)
        order = Order.objects.filter(user=self.request.user).first()
        item = OrderItem.objects.filter(order=order, item=product, user=self.request.user, completed=False)

        if item.exists():
            item = item.first()

            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                return Response({"message": f"Quantity of {item.item.title} decreased by 1"})

            else:
                item.delete()
                return Response({"message": f"{item.item.title} removed from the cart"})

        return Response({"message": f"No related item in the cart"}, status=status.HTTP_404_NOT_FOUND)
