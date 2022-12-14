from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from shop.models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer


"""
4. Add to cart 
5. remove from cart totally
6. remove single from cart

"""


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
                return Response({"message": "Item quantity increased"}, status=status.HTTP_200_OK)

            else:

                user_orderitem = OrderItem.objects.create(
                    user=request.user,
                    item=product,
                    quantity=1,
                )
                current_order.items.add(user_orderitem)

                # return Response(order_serializer.data, status=status.HTTP_200_OK)
                return Response({"message": "Item added to the cart"}, status=status.HTTP_200_OK)

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
            return Response({"message": "Item added to your cart"}, status=status.HTTP_200_OK)


class RemoveFromCart(APIView):
    # item exists in cart
        # remove item totally
    # item doesnt exist
        #do nothing
    pass


class RemoveSingleFromCart(APIView):
    # item exists in cart
        # if item quantity is 1
            # delete item
        # else
            #
    # item doesnt exist
    # do nothing
    pass

