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
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)

    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    age = property(calculate_age)

    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender)

    def str(self):
        return self.user.username
    
    

class Fuel(models.Model):
    fueltype = models.CharField(max_length=255,unique=True)  # Define the field for fuel type
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Define the field for price
    profile_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fueltype
    
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
    

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('COD', 'COD'),
        ('PayPal', 'PayPal'),
    )

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    fuel_type = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    delivery_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True, default='COD')

    def __str__(self):
        return f"Order {self.id} by {self.customer.username} at {self.order_date}"

