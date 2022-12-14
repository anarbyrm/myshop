# Generated by Django 4.1.4 on 2022-12-13 17:15

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="items",
            field=models.ManyToManyField(blank=True, to="shop.orderitem"),
        ),
        migrations.AlterField(
            model_name="order",
            name="ref_code",
            field=models.CharField(
                default=shop.models.ref_code_generator, max_length=15
            ),
        ),
    ]
