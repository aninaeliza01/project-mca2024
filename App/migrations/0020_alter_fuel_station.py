# Generated by Django 4.2.5 on 2023-11-13 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0019_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuel',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fuels', to='App.fuelstation'),
        ),
    ]
