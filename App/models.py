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

    user_type = models.CharField(max_length=20,choices=USER_TYPES,blank=True, null=True)
    
    # USERNAME_FIELD  = 'email'
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, unique=True,blank=True, null=True)
    password = models.CharField(max_length=128)

    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_deliveryteam = models.BooleanField(default=False)

    gstn = models.CharField(max_length=15, blank=True, null=True ,unique=True)  # GSTN field
    dln = models.CharField(max_length=15, blank=True, null=True ,unique=True)  # DL field

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
    
    from django.db import models

class Fuel(models.Model):
    fueltype = models.CharField(max_length=255)  # Define the field for fuel type
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Define the field for price
    profile_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fueltype
    
class LocationDetails(models.Model):
    name = models.CharField(max_length=255)  # Define the field for fuel type
    def __str__(self):
        return self.name
    
class PumpDetails(models.Model):
    name = models.CharField(max_length=255)  # Define the field for fuel type
    location= models.ForeignKey(LocationDetails,on_delete=models.CASCADE,related_name='pumb') # Define the field for price
    valueaddedservice = models.CharField(max_length=255,blank=True, null=True)
    

    def __str__(self):
        return self.name
