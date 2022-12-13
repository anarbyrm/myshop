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
    slug = models.SlugField()


    def __str__(self) -> str:
        return self.title


class OrderItem(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f'{self.user}: {self.quantity} of {self.product}'


class Order(BaseModel):
    UUID = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    completed = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f'{self.user.username}: {self.ref_code}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.ref_code = ref_code_generator()

        return super().save(*args, **kwargs)
    


