# Generated by Django 4.1.4 on 2022-12-14 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_orderitem_completed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(unique=True),
        ),
    ]