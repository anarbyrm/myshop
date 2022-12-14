from django.urls import path

from .views import (
    ProductList,
    ProductDetail,
    OrderView,
)


urlpatterns = [
    path("", ProductList.as_view()),
    path("products/<slug>/", ProductDetail.as_view()),
    path("order/<uuid>/", OrderView.as_view())

]