from django.db import models
from django.conf import settings

import random
import string
from uuid import uuid4


def refund_code_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class BaseModel(models.Model):
    pass


class ProductCategory(BaseModel):
    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title


class ProductSubcategory(BaseModel):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title


class ProductType(BaseModel):
    subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title


class Size(BaseModel):
    value = models.CharField(max_length=5)

    def __str__(self):
        return self.value


class ProductReview(BaseModel):
    RATING_CHOICES = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5)
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    comment = models.TextField(null=True, blank=True)
    item = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    def __str__(self):
        return f'{self.user} gave {self.rating} stars to {self.item}'

    class Meta:
        unique_together = ('user', 'item')


class ProductImage(BaseModel):
    file = models.ImageField(upload_to='images/products/additional/')
    item = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='photos',
    )


class Product(BaseModel):
    # type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/product/')
    size = models.ManyToManyField(Size, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def get_overall_rating(self):
        total = sum(int(review.rating) for review in self.reviews.all())
        if total > 0:
            count = self.reviews.count()
            return total / count
        return 0


class OrderItem(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('cart', 'item')
        ordering = ('completed', 'cart')

    def __str__(self) -> str:
        return f'{self.user}: {self.quantity} of {self.item}'

    def get_total_price(self):
        return self.item.price * self.quantity


class Order(BaseModel):
    STATUS_CHOICES = (
        ('P', 'Preparing'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
    )

    UUID = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    refund_code = models.CharField(max_length=15, default=refund_code_generator)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username}: {self.refund_code}'

    def get_total_items(self):
        total_count = 0
        for item in self.items.all():
            total_count += item.quantity
        return total_count

    def get_total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.get_total_price()

        return total_price


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    address = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=225)
    use_later = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s address"


