# Generated by Django 4.0.3 on 2022-04-04 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0013_restaurant_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='owner',
            field=models.OneToOneField(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='my_restaurants', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
