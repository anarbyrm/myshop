# Generated by Django 4.1.4 on 2022-12-22 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shop.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        to="shop.basemodel",
                    ),
                ),
                (
                    "UUID",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("completed", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("P", "Preparing"),
                            ("S", "Shipped"),
                            ("D", "Delivered"),
                        ],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("date_ordered", models.DateTimeField(auto_now_add=True)),
                (
                    "refund_code",
                    models.CharField(
                        default=shop.models.refund_code_generator, max_length=15
                    ),
                ),
                ("refund_requested", models.BooleanField(default=False)),
                ("refund_granted", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("shop.basemodel",),
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="shop.basemodel",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="images/product/")),
                ("color", models.CharField(blank=True, max_length=50, null=True)),
                ("in_stock", models.BooleanField(default=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("slug", models.SlugField(unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            bases=("shop.basemodel",),
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="shop.basemodel",
                    ),
                ),
                ("title", models.CharField(max_length=70)),
            ],
            bases=("shop.basemodel",),
        ),
        migrations.CreateModel(
            name="ProductSubcategory",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="shop.basemodel",
                    ),
                ),
                ("title", models.CharField(max_length=70)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shop.productcategory",
                    ),
                ),
            ],
            bases=("shop.basemodel",),
        ),
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="shop.basemodel",
                    ),
                ),
                ("value", models.CharField(max_length=5)),
            ],
            bases=("shop.basemodel",),
        ),
        migrations.CreateModel(
            name="ProductType",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="shop.basemodel",
                    ),
                ),
                ("title", models.CharField(max_length=70)),
                (
                    "subcategory",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shop.productsubcategory",
                    ),
                ),
            ],
            bases=("shop.basemodel",),
        ),
        migrations.CreateModel(
            name="ProductReview",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="shop.basemodel",
                    ),
                ),
                (
                    "rating",
                    models.CharField(
                        choices=[("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)],
                        max_length=1,
                    ),
                ),
                ("comment", models.TextField(blank=True, null=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="shop.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("shop.basemodel",),
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="shop.basemodel",
                    ),
                ),
                ("file", models.ImageField(upload_to="images/products/additional/")),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="shop.product",
                    ),
                ),
            ],
            bases=("shop.basemodel",),
        ),
        migrations.AddField(
            model_name="product",
            name="size",
            field=models.ManyToManyField(blank=True, to="shop.size"),
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="shop.basemodel",
                    ),
                ),
                ("quantity", models.PositiveSmallIntegerField()),
                ("completed", models.BooleanField(default=False)),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="shop.order",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="shop.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("cart", "item")},
            },
            bases=("shop.basemodel",),
        ),
    ]
