# Generated by Django 4.2.5 on 2023-11-30 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0022_remove_payment_razor_pay_payment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.fuelstation'),
        ),
    ]