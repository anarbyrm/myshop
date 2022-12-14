from django.urls import path

from .views import (
    ProductList,
    ProductDetail,
    OrderView,
    AddToCart,
    RemoveAllFromCart,
    RemoveSingleFromCart

)


urlpatterns = [
    path("", ProductList.as_view()),
    path("<slug>/", ProductDetail.as_view()),
    path("<slug>/add-to-cart/", AddToCart.as_view()),
    path("<slug>/remove-all/", RemoveAllFromCart.as_view()),
    path("<slug>/remove-single/", RemoveSingleFromCart.as_view()),
    path("my-order/<uuid>/", OrderView.as_view()),
]