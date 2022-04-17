# Generated by Django 4.0.3 on 2022-04-13 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0009_alter_employee_first_name_alter_employee_last_name'),
        ('api', '0020_alter_restaurant_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_restaurants', to='user_management.employee'),
        ),
    ]