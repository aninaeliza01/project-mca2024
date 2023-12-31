from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
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
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE, blank=True, null=True, related_name='fuels')
    profile_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fueltype  


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
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    delivery_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True, default='COD')

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
    
class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)