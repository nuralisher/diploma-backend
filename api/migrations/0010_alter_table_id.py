# Generated by Django 4.0.3 on 2022-03-23 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_table_qr_code_alter_table_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]