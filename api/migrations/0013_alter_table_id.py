# Generated by Django 4.0.3 on 2022-03-23 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_table_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
