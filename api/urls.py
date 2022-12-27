from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)