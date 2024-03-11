from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.db.models import Q
# Create your models here.
class CustomUser(AbstractUser):

    USER_TYPES = (
        ('ADMIN','Admin'),
        ('VENDOR', 'Vendor'),
        ('DELIVERYTEAM', 'Deliveryteam'),
        ('CUSTOMER', 'Customer'),
    )

    user_type = models.CharField(max_length=20,choices=USER_TYPES,blank=True, null=True, default='CUSTOMER')
    
    # USERNAME_FIELD  = 'email'
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, unique=True,blank=True, null=True)
    password = models.CharField(max_length=128)

    is_customer = models.BooleanField(default=True)
    is_vendor = models.BooleanField(default=False)
    is_deliveryteam = models.BooleanField(default=False)


    REQUIRED_FIELDS = []
    def _str_(self):
        return self.username 

class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.user.username
    
    
class LocationDetails(models.Model):
    name = models.CharField(max_length=255,unique=True)  # Define the field for fuel type
    def __str__(self):
        return self.name
    
# class PumpDetails(models.Model):
#     name = models.CharField(max_length=255)  # Define the field for fuel type
#     location= models.ForeignKey(LocationDetails,on_delete=models.CASCADE,related_name='pumb') # Define the field for price
#     valueaddedservice = models.CharField(max_length=255,blank=True, null=True)
    

#     def __str__(self):
#         return self.name

class FuelStation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=100)
    ownername = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    location= models.ForeignKey(LocationDetails,on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    gst_number = models.CharField(max_length=15)
    logo_image = models.ImageField(upload_to='media/fuel_station_logos', blank=True, null=True)

    def __str__(self):
        return self.station_name
    
class Fuel(models.Model):
    fueltype = models.CharField(max_length=255)  
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE, blank=True, null=True, related_name='fuels')
    profile_modified_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        # Calculate the sale price based on the discount and price
        self.sale_price = self.price - (self.price * (self.discount / 100))

        super(Fuel, self).save(*args, **kwargs)


    def __str__(self):
        return self.fueltype  

    
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MapLocation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pump_lat = models.DecimalField(max_digits=9, decimal_places=6)
    pump_lng = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_area_lat = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_area_lng = models.DecimalField(max_digits=9, decimal_places=6)

from django.utils import timezone

class DeliveryTeam(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    location= models.ForeignKey(LocationDetails,on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    vehno = models.CharField(max_length=15,unique=True,)
    propic = models.ImageField(upload_to='media/delivery_pic', blank=True, null=True)
    drivelic = models.ImageField(upload_to='media/driving_license', blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_checkin = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)


class CheckInOutRecord(models.Model):
    delivery_team = models.ForeignKey(DeliveryTeam, on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(default=timezone.now)
    checkout_time = models.DateTimeField(blank=True, null=True)

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('COD', 'COD'),
        ('PayPal', 'PayPal'),
    )

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    fuel_type = models.ForeignKey(Fuel, on_delete=models.CASCADE, blank=True, null=True)
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    itemprice=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deliveryprice=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    delivery_address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True, default='COD')
    delivery_team = models.ForeignKey(DeliveryTeam, on_delete=models.SET_NULL, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # New field for storing QR code image

    def __str__(self):
        return f"Order {self.id} by {self.customer.username} at {self.order_date}"
    
class Payment(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id=models.CharField(max_length=100, blank=True, null=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the payment to a customer
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Store the payment amount
    payment_date = models.DateTimeField(auto_now_add=True)  # Date and time of the payment
    # Add other fields as per your requirements, like payment status, transaction ID, etc.
    
    def __str__(self):
        return f"Payment of {self.amount} by {self.customer.username} on {self.payment_date}"
    


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)