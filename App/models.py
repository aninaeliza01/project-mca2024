from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username, phone, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, password=None):
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.user_type=1
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    ADMIN=1
    VENDOR=2
    DELIVERYTEAM=3
    CUSTOMER=4

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (VENDOR, 'Vendor'),
        (DELIVERYTEAM, 'Deliveryteam'),
        (CUSTOMER, 'Customer'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default='4')
    username=models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=128)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
      
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
    
    def get_role(self): 
        if self.user_type == 2:
            user_role = 'Vendor'
        elif self.user_type == 3:
            user_role = 'Deliveryteam'
        elif self.user_type == 4:
            user_role = 'Customer'
        return user_role
