# Generated by Django 4.2.5 on 2023-09-28 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Vendor'), (3, 'Deliveryteam'), (4, 'Customer')], default='4'),
        ),
    ]
