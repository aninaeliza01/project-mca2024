# Generated by Django 4.2.5 on 2023-11-03 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_order_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]