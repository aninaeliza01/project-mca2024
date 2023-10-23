# Generated by Django 4.2.5 on 2023-10-23 10:01

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fueltype', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profile_modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocationDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(blank=True, choices=[('ADMIN', 'Admin'), ('VENDOR', 'Vendor'), ('DELIVERYTEAM', 'Deliveryteam'), ('CUSTOMER', 'Customer')], default='CUSTOMER', max_length=20, null=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('is_customer', models.BooleanField(default=True)),
                ('is_vendor', models.BooleanField(default=False)),
                ('is_deliveryteam', models.BooleanField(default=False)),
                ('gstn', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('dln', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='media/profile_picture')),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('addressline1', models.CharField(blank=True, max_length=50, null=True)),
                ('addressline2', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('profile_created_at', models.DateTimeField(auto_now_add=True)),
                ('profile_modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FuelStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=100)),
                ('ownername', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=12)),
                ('gst_number', models.CharField(max_length=15)),
                ('logo_image', models.ImageField(blank=True, null=True, upload_to='fuel_station_logos/')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.locationdetails')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
