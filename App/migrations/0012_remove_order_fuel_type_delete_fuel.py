# Generated by Django 4.2.5 on 2023-11-11 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_rename_cancel_order_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='fuel_type',
        ),
        migrations.DeleteModel(
            name='Fuel',
        ),
    ]
