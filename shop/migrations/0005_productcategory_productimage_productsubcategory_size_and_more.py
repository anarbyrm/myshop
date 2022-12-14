# Generated by Django 4.1.4 on 2022-12-14 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0004_alter_product_slug"),
    ]

    operations = [
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
        migrations.AddField(
            model_name="product",
            name="color",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(
                default=django.utils.timezone.now, upload_to="images/product/"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="in_stock",
            field=models.BooleanField(default=True),
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
                        choices=[
                            (1, "Very Bad"),
                            (2, "Bad"),
                            (3, "Mediocre"),
                            (4, "Good"),
                            (5, "Excellent"),
                        ],
                        max_length=1,
                    ),
                ),
                ("comment", models.TextField(blank=True, null=True)),
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
        migrations.AddField(
            model_name="product",
            name="additional_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="photos",
                to="shop.productimage",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="review",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reviews",
                to="shop.productreview",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="size",
            field=models.ManyToManyField(blank=True, to="shop.size"),
        ),
    ]
