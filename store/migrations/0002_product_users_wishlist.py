# Generated by Django 4.2 on 2023-05-26 13:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="users_wishlist",
            field=models.ManyToManyField(
                blank=True, related_name="user_wishlist", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
