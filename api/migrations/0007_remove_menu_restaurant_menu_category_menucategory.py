# Generated by Django 4.0.3 on 2022-03-30 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_menu_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='menu',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='api.restaurant'),
        ),
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='api.restaurant')),
            ],
        ),
    ]
