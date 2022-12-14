from django.db import models
from django.conf import settings

import random
import string
from uuid import uuid4


def ref_code_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class BaseModel(models.Model):
    pass


class Product(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField() 
    price = models.DecimalField(decimal_places=2, max_digits=10)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.title

    # def get_absolute_url(self):
    #     # return reverse("model_detail", kwargs={"pk": self.pk})
    #     pass

    # def get_add_to_cart_url(self):
    #     pass

    # def get_remove_all_from_cart_url(self):
    #     pass

    # def get_remove_single_from_cart_url(self):
    #     pass


class OrderItem(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user}: {self.quantity} of {self.item}'

    def get_total_price(self):
        return self.item.price * self.quantity


class Order(BaseModel):
    UUID = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, blank=True)
    completed = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=15, default=ref_code_generator)

    def __str__(self) -> str:
        return f'{self.user.username}: {self.ref_code}'

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

    # def get_empty_the_cart_url(self):
    #     pass
    


