from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import FuelForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# from django.contrib.auth.models import User
# Create your views here.
@never_cache
def index(request):
    fuels = Fuel.objects.all()  # Retrieve fuel records
    user = request.user
    context = {
        'fuels': fuels,
        'user':user,
        # Other context data
    }
    return render(request, 'index.html', context)

@never_cache
@login_required(login_url='login')
def userhome(request):
    pumps = FuelStation.objects.all() 
    context = {'pumps': pumps}
    return render(request, 'userhome.html', context)

def place_order(request, pump_id):
    fuel_types = Fuel.objects.all()
    pump = get_object_or_404(FuelStation, pk=pump_id)
    context = {
        'fuel_types': fuel_types,
        'pump': pump
        # Include other context data you need
    }


    return render(request, 'place_order.html', context)
def userBase(request):
    return render(request,'userBase.html')


from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from .tokens import account_activation_token
from .models import CustomUser, UserProfile  # Make sure to import your models
from django.contrib.sites.models import Site

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Check if the user is already active
        if user.is_active:
            messages.warning(request, "Your account is already activated. You can log in.")
            return redirect('login')

        elif account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "Thank you for confirming your email. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or has expired. Please request a new one.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Activation link is invalid. Please request a new one.")

    return redirect('login')
def activateEmail(request, user):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user, 
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    to_email = user.email  # Get the user's email from the user object
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user.username}, please go to your email {to_email} inbox and click on \
                the received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
# @never_cache
# def register_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         email = request.POST.get('email', None)
#         phone = request.POST.get('phoneNumber', None)
#         password = request.POST.get('password', None)
#         confirm_password = request.POST.get('cpassword', None)
       
#         user_type = 'CUSTOMER'

#         # Validate the email
#         # try:
#         #     validate_email(email)
#         # except ValidationError:
#         #     messages.error(request, "Invalid email address.")
#         #     return render(request, 'registerUser.html')

#         if username and email and password:
#             if CustomUser.objects.filter(email=email).exists():
#                 messages.success(request, "Email is already registered.")
#                 return redirect('registerUser')
#             elif CustomUser.objects.filter(username=username).exists():
#                 messages.success(request, "Username is already registered.")
#                 return redirect('registerUser')
#             elif password != confirm_password:
#                 messages.success(request, "Passwords don't match. Please enter correct passwords.")
#                 return redirect('registerUser')
#             else:
#                 user = CustomUser(username=username, email=email, user_type=user_type,phone=phone)
#                 user.set_password(password)  # Set the password securely
#                 user.is_active = False
#                 user.is_customer = True
#                 user.user_type = user_type
#                 user.save()
#                 user_profile = UserProfile(user=user)
#                 user_profile.save()
#                 activateEmail(request, user)
#                 userFuel = FuelStation(user=user)
#                 userFuel.station_name = request.POST.get('station_name')
#                 userFuel.ownername = request.POST.get('ownername')
#                 userFuel.address = request.POST.get('address')
#                 userFuel.email = email
#                 userFuel.phone_number = phone
#                 userFuel.gst_number = gstn
#                 userFuel.logo_image = request.FILES.get('logo_image')
#                 userFuel.location = LocationDetails.objects.get(pk=request.POST.get('location'))
#                 userFuel.save()

#                 return redirect('login')

#     return render(request, 'registerUser.html')

@never_cache
def login_user(request):
            # # if request.user.is_authenticated:
            # #     return redirect('/')
            # if 'username' in request.session:
            #     return redirect('/userhome')
            # elif 'username' in request.session:
            #     return redirect('/pumphome')
            # elif 'username' in request.session:
            #     return redirect('/adminhome')

        
        
            if request.method == 'POST':
                username = request.POST["username"]
                password = request.POST["password"]
                if username and password:
                    user = authenticate(request, username =username , password=password)

                    if user is not None:
                        auth_login(request, user)
                        print(request.user.is_customer, "1")
                        if user.is_customer:
                            request.session["username"] = user.username  # Use single equal sign (=) here
                            return redirect('/userhome')
                        elif user.is_vendor:
                            request.session["username"] = user.username
                            return redirect('/pumphome')
                        elif user.is_superuser:
                            request.session["username"] = user.username
                            return redirect('/adminhome')
                    else:
                          messages.success(request,("Invalid credentials."))
                          return redirect('/login')
                else:
                     messages.success(request,("Please fill out all fields."))
                     return redirect('/login')

            return render(request, 'login.html')

@login_required(login_url='login')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')

@login_required(login_url='login')
def customer_Profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile = None  # Initialize profile with a default value

    if request.method == 'POST':
        # Update the user profile fields directly from the form data
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile.profile_picture = profile_picture

        
        user_profile.address = request.POST.get('address')
        user_profile.addressline1 = request.POST.get('addressline1')
        user_profile.addressline2 = request.POST.get('addressline2')
        user_profile.state = request.POST.get('state')
        user_profile.city = request.POST.get('city')
        user_profile.pin_code = request.POST.get('pin_code')
        user_profile.gender = request.POST.get('gender')
        user_profile.dob = request.POST.get('dob')
        user_profile.save()
        messages.success(request, 'Profile updated successfully')

    user_details = CustomUser.objects.filter(id=request.user.id).values('username', 'email', 'phone').first()

    context = {
        'user_profile': user_profile,
        'user_details': user_details, # Assign the value of 'profile' here
    }

    return render(request, 'profile.html', context)

@never_cache
def register_pump(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phoneNumber', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('cpassword', None)
        gstn=request.POST.get('gstNumber',None)
        user_type='VENDOR'
        # user_type = CustomUser.is_vendor
        if username and email and phone and password:
            if CustomUser.objects.filter(email=email).exists():
                messages.success(request,("Email is already registered."))
            elif CustomUser.objects.filter(username=username).exists():
                messages.success(request,("Username is already registered."))
            elif password!=confirm_password:
                messages.success(request,("Password's Don't Match, Enter correct Password"))
            else:
                user = CustomUser(username=username, email=email, phone=phone,gstn=gstn,user_type=user_type)
                user.set_password(password)  # Set the password securely
                user.is_active=False
                user.is_vendor=True
                user.is_customer = False
                user.save()
                userFuel = FuelStation(user=user)
                userFuel.station_name = request.POST.get('station_name')
                userFuel.ownername = request.POST.get('ownername')
                userFuel.address = request.POST.get('address')
                userFuel.email = email
                userFuel.phone_number = phone
                userFuel.gst_number = gstn
                userFuel.location = LocationDetails.objects.get(pk=request.POST.get('location'))
                userFuel.logo_image = request.FILES.get('logo_image')
                userFuel.save()
                activateEmail(request, user)
                return redirect('login') 
    locations = LocationDetails.objects.all()
    return render(request, 'registerPump.html', {'locations': locations})

# @never_cache
# @login_required(login_url='login')
# def userhome(request):
#     if request.user.is_customer:
#         content=Fuel.objects.all()
#         # fueltype = 
#         # price = 
#         context={
#             'fueltype':content
#         }
#         return render(request,'userhome.html',context)
#     return redirect('/login')
    # return redirect('log')
@never_cache
@login_required(login_url='login')
def pumphome(request):
    if request.user.is_vendor == True:
    # if request.user.is_authenticated:
        return render(request,'pumphome.html')
    return redirect('/login')
    # return redirect('log')



def base(request):
    return render(request, 'base.html')

def adminbase(request):
    return render(request, 'adminBase.html')

@never_cache
@login_required(login_url='login')
def adminuser(request):
    users = CustomUser.objects.all()
    context = {
       'users':users  
     }
    return render(request, 'adminUser.html',context)
@never_cache
@login_required(login_url='login')
def block_unblock_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    if user.is_active:
        user.is_active = False  # Block the user
        subject = 'Account Blocked'
        message = 'Your account has been blocked by the admin.'
        from_email = 'aninaelizebeth2024a@mca.ajce.in'  # Use your admin's email address
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    else:
        user.is_active = True  # Unblock the user
    user.save()
    return redirect('/adminuser') 

@never_cache
@login_required(login_url='login')
def adminpump(request):  
    users = CustomUser.objects.all()
    context = {
       'users':users  
     }  
    return render(request, 'adminPump.html',context)

@never_cache
@login_required(login_url='login')
def fuel(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = FuelForm(request.POST)
            if form.is_valid():
                form.save()
                # Redirect to the admin dashboard page after successfully saving the data
                return redirect('fuel')
    fuels = Fuel.objects.all()
    form = FuelForm()
    context = {
    'fuels': fuels,
    'form': form, # Pass the user count to the template
    }
    return render(request, 'fuel.html',context)

@never_cache
@login_required(login_url='login')
def location(request):
    if request.method == "POST":
        name = request.POST.get("name")
        LocationDetails.objects.create(name=name)
    
    locations = LocationDetails.objects.all()
    
    return render(request, "location.html", {"locations": locations})

@never_cache
@login_required(login_url='login')
def adminhome(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = FuelForm(request.POST)
            if form.is_valid():
                form.save()
                # Redirect to the admin dashboard page after successfully saving the data
                return redirect('/adminhome')
    
    users = CustomUser.objects.all()
    user_count = users.count()  # Calculate the count of users

    fuels = Fuel.objects.all()
    form = FuelForm()
    context = {
        'users': users,
        'user_count': user_count, 
        'fuels': fuels,
        'form': form, # Pass the user count to the template
        
    }
    return render(request, 'ad.html',context)

@never_cache
@login_required(login_url='login')
def update_fuel(request, fuel_id):
    fuel = get_object_or_404(Fuel, pk=fuel_id)

    if request.method == 'POST':
        # Get the updated values from the POST request
        fuel.price = request.POST.get('price')
        # if(fuel.price<=0):

        # Save the updated fuel object
        fuel.save()

        return redirect('fuel')  # Redirect to the fuel records page after updating

    return render(request, 'fuel.html', {'fuel': fuel})


