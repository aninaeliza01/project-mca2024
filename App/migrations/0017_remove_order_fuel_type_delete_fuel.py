# Generated by Django 4.2.5 on 2023-11-11 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0016_alter_fuel_fueltype'),
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
