from django.shortcuts import *
from .models import *

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

from django.db.models import Avg
@never_cache
@login_required(login_url='login')
def userhome(request):
    users = CustomUser.objects.filter(is_active=True)
    active_pumps = FuelStation.objects.filter(user__is_active=True)
    
    # Annotate each FuelStation with its average rating
    pumps_with_avg_rating = active_pumps.annotate(avg_rating=Avg('rating__value'))

    context = {
        'pumps': pumps_with_avg_rating,
        'users': users,
    }
    return render(request, 'userhome.html', context)



@never_cache
@login_required(login_url='login')
def fuel_station_detail(request, station_id):
    station = get_object_or_404(FuelStation, pk=station_id)
    fuels = Fuel.objects.filter(station=station)
    ratings = Rating.objects.filter(station=station)

    context = {
        'station': station,
        'fuels': fuels,
        'ratings': ratings,
    }

    return render(request, 'fuel_station_detail.html', context)


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

@never_cache
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phoneNumber', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('cpassword', None)
       
        user_type = 'CUSTOMER'

        # Validate the email
        # try:
        #     validate_email(email)
        # except ValidationError:
        #     messages.error(request, "Invalid email address.")
        #     return render(request, 'registerUser.html')

        if username and email and password:
            if CustomUser.objects.filter(email=email).exists():
                messages.success(request, "Email is already registered.")
                return redirect('registerUser')
            elif CustomUser.objects.filter(username=username).exists():
                messages.success(request, "Username is already registered.")
                return redirect('registerUser')
            elif password != confirm_password:
                messages.success(request, "Passwords don't match. Please enter correct passwords.")
                return redirect('registerUser')
            else:
                user = CustomUser(username=username, email=email, user_type=user_type,phone=phone)
                user.set_password(password)  # Set the password securely
                user.is_active = False
                user.is_customer = True
                user.user_type = user_type
                user.save()
                user_profile = UserProfile(user=user)
                user_profile.save()
                activateEmail(request, user)

                return redirect('login')

    return render(request, 'registerUser.html')

@never_cache
def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
        # Example redirection based on session (commented out)
        # if 'username' in request.session:
        #     return redirect('/userhome')
        # elif 'username' in request.session:
        #     return redirect('/pumphome')
        # elif 'username' in request.session:
        #     return redirect('/adminhome')

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if user.is_customer:
                    request.session["username"] = user.username
                    return redirect('/userhome')
                elif user.is_vendor:
                    request.session["username"] = user.username
                    return redirect('/pumphome')
                elif user.is_superuser:
                    request.session["username"] = user.username
                    return redirect('/adminhome')
            else:
                # Invalid credentials - user not authenticated
                messages.error(request, "Invalid credentials.")
                return redirect('/login')
        else:
            # Handle the case where username or password is missing
            messages.error(request, "Please provide both username and password.")
            return redirect('/login')
    
    return render(request, 'login.html')


@login_required(login_url='login')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')


@never_cache
@login_required(login_url='login')
def customer_Profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_details = CustomUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        # Update the user profile fields directly from the form data
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile.profile_picture = profile_picture
            user_profile.save()
            # messages.success(request, 'Profile picture updated successfully')

        username = request.POST.get('username')
        phone = request.POST.get('phone')

        user_details.username = username
        user_details.phone = phone

        user_profile.address = request.POST.get('address')
        # Update other profile fields as needed

        user_profile.save()
        user_details.save()
        messages.success(request, 'Profile updated successfully')

    # The rest of your view logic

    context = {
        'user_profile': user_profile,
        'user_details': user_details,
    }

    return render(request, 'profile.html', context)

from django.contrib.auth import update_session_auth_hash
@never_cache
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Check if the current password is correct
        if request.user.check_password(current_password):
            if new_password == confirm_new_password:
                # Update the user's password
                request.user.set_password(new_password)
                request.user.save()
                
                # Ensure the user stays logged in
                update_session_auth_hash(request, request.user)
                
                messages.success(request, 'Password changed successfully')
                return redirect('logout')
            else:
                messages.error(request, 'New passwords do not match')
        else:
            messages.error(request, 'Incorrect current password')
    
    return render(request, 'changePassword.html',)

@never_cache
def register_pump(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phoneNumber', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('cpassword', None)
        gstn=request.POST.get('gstNumber',None)
        image = request.FILES.get('logo_image')
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
                user = CustomUser(username=username, email=email, phone=phone,user_type=user_type)
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
                userFuel.logo_image = image
                
                userFuel.save()
                activateEmail(request, user)
                return redirect('login') 
    locations = LocationDetails.objects.all()
    return render(request, 'registerPump.html', {'locations': locations})

@never_cache
@login_required(login_url='login')
def pumphome(request):
    if request.user.is_vendor:
        fuel_station = request.user.fuelstation

        if fuel_station:
            pump_orders = Order.objects.filter(station=fuel_station, is_ordered=True)

            total_order_count = pump_orders.count()
            accepted_order_count = pump_orders.filter(is_accepted=True).count()
            delivered_order_count = pump_orders.filter(is_delivered=True).count()

            return render(request, 'pumphome.html', {
                'pump_orders': pump_orders,
                'fuel_station': fuel_station,
                'total_order_count': total_order_count,
                'accepted_order_count': accepted_order_count,
                'delivered_order_count': delivered_order_count
            })

@never_cache
@login_required(login_url='login')        
def order(request):
    if request.user.is_vendor:
        # Retrieve the FuelStation instance associated with the user
        fuel_station = request.user.fuelstation  # Assuming this is the attribute that holds the FuelStation reference for the user

        if fuel_station:
            # Fetch orders associated with this station
            pump_order = Order.objects.filter(station=fuel_station, is_ordered=True)
            pump_orders = list(reversed( pump_order))
            
            items_per_page = 10
            paginator = Paginator(pump_orders, items_per_page)

            # Get the current page number from the request's GET parameters
            page = request.GET.get('page')

            try:
                # Get the orders for the current page
                pump_orders = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver the first page
                pump_orders = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g., 9999), deliver the last page
                pump_orders = paginator.page(paginator.num_pages)



            return render(request, 'Fuelorder.html', {'pump_orders': pump_orders, 'fuel_station': fuel_station})
        
@never_cache
@login_required(login_url='login')  
def accept_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order.is_accepted = True
        order.is_ordered = True  # Assuming is_ordered means the order is confirmed or accepted
        order.save()
        station_email=order.station.email
        customer_email = order.customer.email  # Assuming 'customer' is the ForeignKey field
        email_subject = 'Order Accepted'
        email_body = '''
        Dear Customer,

        We are pleased to inform you that your order has been accepted. Thank you for choosing Hybrid Energy.

        To proceed further, kindly make the payment as soon as possible. Should you encounter any difficulties or require assistance with the payment process, feel free to reach out to us. Our team is here to assist you.

        Thank you for your trust in Hybrid Energy. We look forward to delivering an exceptional service and ensuring a seamless experience for you.

        Best Regards,
        Hybrid Energy Team
        '''

        # Send the email
        send_mail(
            email_subject,
            email_body,
            station_email,  # Replace with your email
            [customer_email],  # Email of the customer
            fail_silently=False,
        )
        return redirect('orders')  # Redirect to the pump home page after accepting the order

@never_cache
@login_required(login_url='login')
def reject_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        order.is_rejected = True  # Set the order status as not accepted or rejected
        order.save()
        customer_email = order.customer.email  # Assuming 'customer' is the ForeignKey field
        station_email=order.station.email
        email_subject = 'Regarding Your Recent Order'

        email_body = '''
        Dear Customer,

        We regret to inform you that your recent order has been rejected. We apologize for any inconvenience caused.

        Should you require further details or wish to discuss this matter, please don't hesitate to contact us. Our team is readily available to assist you and provide any necessary clarification.

        Thank you for considering Hybrid Energy. We value your patronage and hope to serve you better in the future.

        Best Regards,
        Hybrid Energy Team
        '''
        # Send the email
        send_mail(
            email_subject,
            email_body,
            station_email,  # Replace with your email
            [customer_email],  # Email of the customer
            fail_silently=False,
        )
        return redirect('orders')

@never_cache
@login_required(login_url='login')
def delivery(request):
    fuel_station = request.user.fuelstation  # Assuming this is the attribute that holds the FuelStation reference for the user

    if fuel_station:
        # Fetch orders associated with this station
        pump_order = Order.objects.filter(station=fuel_station, is_ordered=True,is_accepted=True)
        pump_orders = list(reversed( pump_order))
        payment_details = Payment.objects.filter(order__in=pump_order)
    
    # Create a dictionary to map payments to their respective orders
        order_payment_mapping = {payment.order_id: payment for payment in payment_details}

        # Add a flag 'is_paid' to each order indicating if it's paid or not
        for order in pump_order:
            order.is_paid = order.id in order_payment_mapping
        
       

        return render(request, 'FuelDelivery.html', {'pump_orders': pump_orders, 'fuel_station': fuel_station})

def mark_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if not order.is_delivered:
        order.is_delivered = True
        order.save()
        customer_email = order.customer.email  # Assuming 'customer' is the ForeignKey field
        email_subject = 'Your Order Has Been Successfully Delivered'
        email_body = '''
        Dear Customer,

        We are thrilled to inform you that your recent order has been successfully delivered. Thank you for choosing Hybrid Energy as your trusted fuel provider.

        Your satisfaction is paramount to us, and we hope that our service has exceeded your expectations. Should you have any further inquiries or require assistance, please do not hesitate to reach out to us.

        We appreciate your patronage and look forward to serving you again. Fuel your journey with confidence!

        Best Regards,
        Hybrid Energy Team
        '''
        send_mail(
            email_subject,
            email_body,
            'aninaelizebeth2024a@mca.ajce.in',  # Replace with your email
            [customer_email],  # Email of the customer
            fail_silently=False,
        )
    
    # Redirect to the same page or wherever appropriate after marking as delivered
    return redirect('fuelDelivery')

@never_cache
@login_required(login_url='login')
def station_ratings(request):
    station = get_object_or_404(FuelStation, user=request.user)
    ratings = Rating.objects.filter(station=station)

    context = {
        'station': station,
        'ratings': ratings,
    }
    return render(request, 'Fuelratings.html', context)

@never_cache
@login_required(login_url='login')
def fuel_station_profile(request):
    fuel_station = get_object_or_404(FuelStation, user=request.user)
    user_details = CustomUser.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        if 'logo_image' in request.FILES:
            fuel_station.logo_image = request.FILES['logo_image']
        
        fuel_station.phone_number = request.POST.get('phone_number', '')
        fuel_station.gst_number = request.POST.get('gst_number', '')
        fuel_station.save()
        
        # Update username and phone in user details
        user_details.username = request.POST.get('username', '')
        user_details.phone = request.POST.get('phone_number', '')
        user_details.save()
        
        return redirect('/FuelProfile')  # Redirect to the profile page after saving
    
    context = {
        'fuel_station': fuel_station,
        'user_details': user_details,
    }
    return render(request, 'FuelProfile.html', context)


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

from decimal import Decimal
@never_cache
@login_required(login_url='login')
def place_order(request, pump_id):
    if request.method == 'POST':
        fuel_type_id = request.POST.get('fuel_type_id')
        quantity = Decimal(request.POST.get('quantity', '0'))  # Convert quantity to Decimal
        delivery_point = request.POST.get('delivery_point')
        payment_method = request.POST.get('payment_method')

        selected_fuel = get_object_or_404(Fuel, pk=fuel_type_id)
        price_per_liter = selected_fuel.price

        total_price = quantity * price_per_liter  # Calculate total price

        # Assuming the user is logged in, replace this with your authentication logic
        if request.user.is_authenticated:
            customer = request.user
        else:
            # Handle unauthenticated user case as needed
            customer = None

        # Assuming 'station' is defined elsewhere or retrieved
        station = get_object_or_404(FuelStation, pk=pump_id)

        order = Order.objects.create(
            customer=customer,
            fuel_type=selected_fuel,
            station=station,
            quantity=quantity,
            total_price=total_price,
            delivery_address=delivery_point,
            payment_method=payment_method,
        )

        # Redirect to a success page or any other appropriate URL after successful order placement
        return redirect('ordersummary',order_id=order.id)  # Replace 'order_success' with your success URL name

    # Render the order placement form
    fuel_types = Fuel.objects.filter(station=pump_id)
    pump = get_object_or_404(FuelStation, pk=pump_id)
    context = {
        'fuel_types': fuel_types,
        'pump': pump
        # Include other context data you need
    }
    return render(request, 'place_order.html', context)

@never_cache
@login_required(login_url='login')
def order_summary(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        order.is_ordered = True
        order.save()
        fuel_station_email = order.station.email  # Assuming 'fuel_station' is the ForeignKey field

        # Sending an email notification to the fuel station
        send_mail(
            'New Order Placed',
            f'An order has been placed for Fuel Station: {order.station.station_name} at {order.order_date}. Quantity: {order.quantity}, Payment Method: {order.payment_method}, Delivery Address: {order.delivery_address}',
            'aninaelizebeth2024a@mca.ajce.in',  # Your email
            [fuel_station_email],  # Email of the fuel station
            fail_silently=False,
        )
        messages.success(request, 'Order placed successfully!')
        return redirect('customer_orders') 
    return render(request, 'orderSummary.html', {'order': order})

@never_cache
@login_required(login_url='login')
def delete_order(request, order_id):
    if request.method == 'POST':
        # Fetch the order and delete it
        order = Order.objects.get(pk=order_id)
        order.is_active=False
        order.save()
        messages.success(request, 'Order canceled successfully!')
        return redirect('customer_unorders') 
    return render(request, 'orderSummary.html')

@never_cache
@login_required(login_url='login')
def customer_orders(request):
    # Fetch ordered orders sorted by order_date in descending order (most recent first)
    ordered_orders = Order.objects.filter(customer=request.user, is_ordered=True).order_by('-order_date')
    
    # Fetch payment details for the filtered ordered orders
    payment_details = Payment.objects.filter(order__in=ordered_orders).values_list('order_id', flat=True)
    
    # Add a flag 'is_paid' to each order indicating if it's paid or not
    for order in ordered_orders:
        order.is_paid = order.id in payment_details

    items_per_page = 10
    paginator = Paginator(ordered_orders, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the orders for the current page
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        orders = paginator.page(paginator.num_pages)

    context = {
        'ordered_orders': orders,
    }

    return render(request, 'customerOrders.html', context)

@never_cache
@login_required(login_url='login')
def rate_station(request, station_id):
    if request.method == 'POST':
        user = request.user
        station = FuelStation.objects.get(pk=station_id)
        value = int(request.POST['rating'])
        comment = request.POST.get('comment', '')

        rating, created = Rating.objects.get_or_create(user=user, station=station, defaults={'value': value, 'comment': comment})

        if not created:
            rating.value = value
            rating.comment = comment
            rating.save()

        return redirect('station_detail', station_id=station_id)
    else:
        return redirect('home')
    

@never_cache
@login_required(login_url='login')
def station_detail(request, station_id):
    station = FuelStation.objects.get(pk=station_id)
    ratings = Rating.objects.filter(station=station)

    return render(request, 'station_detail.html', {'station': station, 'ratings': ratings})



@never_cache
@login_required(login_url='login')
def customer_unorders(request):
    not_ordered_orders = Order.objects.filter(customer=request.user, is_ordered=False)
    orders = list(reversed( not_ordered_orders))
    items_per_page = 10
    paginator = Paginator(orders, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the orders for the current page
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        orders = paginator.page(paginator.num_pages)

    context = {
        'not_ordered_orders': orders,
    }
    return render(request, 'customerUnorder.html', context)


def base(request):
    return render(request, 'base.html')

def adminbase(request):
    return render(request, 'adminBase.html')


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@never_cache
@login_required(login_url='login')
def adminuser(request):
    users = CustomUser.objects.all()
    items_per_page = 10
    paginator = Paginator(users, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the users for the current page
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        users = paginator.page(paginator.num_pages)
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
        message = 'Your account has been blocked by the admin.Hybrid Energy'
        from_email = 'aninaelizebeth2024a@mca.ajce.in'  # Use your admin's email address
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    else:
        user.is_active = True  # Unblock the user
    user.save()
    return redirect('adminpump') 


@never_cache
@login_required(login_url='login')
def adminorder(request):  
    ordered_orders = Order.objects.filter(is_ordered=True)
    orders = list(reversed( ordered_orders))
    items_per_page = 10
    paginator = Paginator(orders, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the orders for the current page
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        orders = paginator.page(paginator.num_pages)

    context = {
        'ordered_orders': orders,
    }
    return render(request, 'adminorder.html',context)

from django.db.models import Count
@never_cache
@login_required(login_url='login')
def adminpump(request):  
    users = CustomUser.objects.all()
    pump = FuelStation.objects.annotate(total_orders=Count('order')).all()
    # Total order count for each station
    total_orders_per_station = FuelStation.objects.annotate(total_orders=Count('order')).values('station_name', 'total_orders')

    items_per_page = 10
    paginator = Paginator(users, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the users for the current page
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        users = paginator.page(paginator.num_pages)

    context = {
       'users':users,
       'pump':pump,  
       'total_orders_per_station': total_orders_per_station,
     }  
    return render(request, 'adminPump.html',context)


@never_cache
@login_required(login_url='login')
def location(request):
    if request.method == "POST":
        name = request.POST.get("name")
        existing_location = LocationDetails.objects.filter(name=name).first()
        
        if existing_location:
            # Location already exists, set an error message
            messages.success(request, 'This location already exists.!')
            return redirect('location') 
           
        else:
            LocationDetails.objects.create(name=name)
        
    
    locations = LocationDetails.objects.all()
    items_per_page = 5  
    paginator = Paginator(locations, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the locations for the current page
        locations = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        locations = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        locations = paginator.page(paginator.num_pages)
    
    return render(request, "location.html", {"locations": locations})

@never_cache
@login_required(login_url='login')
def update_location(request, location_id):
    location = get_object_or_404(LocationDetails, pk=location_id)

    if request.method == 'POST':
        location.name = request.POST.get('name')
        location.save()
        return redirect('location')  # Redirect to the location list page

    return render(request, 'location.html', {'locations': LocationDetails.objects.all()})

@never_cache
@login_required(login_url='login')
def delete_location(request, location_id):
    location = get_object_or_404(LocationDetails, pk=location_id)

    if request.method == 'GET':
        location.delete()
        return redirect('location')  # Redirect to the location list page

    return render(request, 'location.html', {'locations': LocationDetails.objects.all()})

@never_cache
@login_required(login_url='login')
def adminhome(request):
    
    customer_count = CustomUser.objects.filter(user_type='CUSTOMER').count()
    pump_count = CustomUser.objects.filter(user_type='VENDOR').count()
      # Calculate the count of users

    order = Order.objects.all().count()
    # form = FuelForm()
    context = {
        'customer_count': customer_count,
        'pump_count': pump_count, 
        'order': order,
        # 'form': form, # Pass the user count to the template
        
    }
    return render(request, 'ad.html',context)


from django.db.models import Count, Avg
@never_cache
@login_required(login_url='login')
def ratings_by_station(request):
    # Retrieve ratings grouped by stations
    ratings_by_station = Rating.objects.values('station').annotate(
        total_ratings=Count('id'), 
        average_rating=Avg('value')
    )

    station_ratings = []
    for rating_info in ratings_by_station:
        station_id = rating_info['station']
        total_ratings = rating_info['total_ratings']
        average_rating = rating_info['average_rating']

        station = FuelStation.objects.get(pk=station_id)
        station_ratings.append({
            'station': station,
            'total_ratings': total_ratings,
            'average_rating': average_rating,
        })

    return render(request, 'ratings_by_station.html', {'station_ratings': station_ratings})
@never_cache
@login_required(login_url='login')
def fuel(request):
    existing_fuel = None

    if request.user.is_vendor:
        station_id = request.user.id
        station = FuelStation.objects.get(user=station_id)
        if request.method == 'POST':
            fueltype = request.POST.get('fueltype')
            price = request.POST.get('price')

            existing_fuel = Fuel.objects.filter(fueltype=fueltype, station=station).first()

            if existing_fuel:
                messages.error(request, "A fuel of the same type already exists for this station.")
                return redirect('fuel')
            else:
                fuel = Fuel.objects.create(
                    fueltype=fueltype,
                    price=price,
                    station=station
                )

        fuels = Fuel.objects.filter(station=station)
        context = {
            'fuels': fuels,
        }
        return render(request, 'fuel.html', context)


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


@never_cache
@login_required(login_url='login')
def delete_fuel(request, fuel_id):
    fuel = get_object_or_404(Fuel, pk=fuel_id)

    if request.method == 'GET':
        # Delete the fuel object
        fuel.delete()

        return redirect('fuel')  # Redirect to the fuel records page after deleting

    return render(request, 'fuel.html', {'fuel': fuel})



import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import floatformat
@never_cache
@login_required(login_url='login')
def pay(request,order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=order_id)
        client = razorpay.Client(auth=("rzp_test_z8K4I90GdqQLdV", "eXLlGvh3xWgHBaPIX2uIlveV"))

        order_amount = int(order.total_price* 100)  # Example amount
        data = {
            "amount": order_amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{order_id}"  # Use order ID to generate a unique receipt ID
        }
        payment = client.order.create(data=data)
        rupee_amount = floatformat(payment['amount'] / 100, 2)
        # Render the payment page with the payment details
        return render(request, 'pay.html', {'payment': payment, 'order': order, 'rupee_amount': rupee_amount})
   
    return HttpResponse("Invalid request")

@csrf_exempt
def success(request, order_id):
    print("Received payment_id:", order_id)
    order = get_object_or_404(Order, pk=order_id)
    station_id = order.station_id
    
    # Fetch the FuelStation instance associated with the station_id
    station = get_object_or_404(FuelStation, pk=station_id)
    client = razorpay.Client(auth=("rzp_test_z8K4I90GdqQLdV", "eXLlGvh3xWgHBaPIX2uIlveV"))

    order_amount = int(order.total_price* 100)  # Example amount
    data = {
        "amount": order_amount,
        "currency": "INR",
        "receipt": f"order_rcptid_{order_id}"  # Use order ID to generate a unique receipt ID
    }
    payment = client.order.create(data=data)
       
    # Retrieve the payment instance you want to update
    
    payment = client.order.create(data=data)

    # payment = get_object_or_404(Payment, order_id=order)
    order_amount = int(order.total_price* 100) 
    new_payment = Payment(
            order=order,
            razor_pay_order_id=payment['id'],
            amount=order_amount,
            is_paid = True,
            station=station,
            customer=request.user  # Assuming the user is authenticated and initiating the payment
        )
    new_payment.save()

    

    messages.success(request, 'Payment successfully done.')
    return redirect('customer_orders')


from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Order, Payment

def generate_receipt_pdf(order_id):
    order = get_object_or_404(Order, pk=order_id)
    payment = get_object_or_404(Payment, order=order)

    buffer = BytesIO()

    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter, title="HybridEnergy")

    # Title
    title_style = ParagraphStyle(
        name='TitleText',
        alignment=1,
        fontSize=20
    )
    title_text = Paragraph("Receipt for HybridEnergy", title_style)
    
    receipt_details = [
        ["Order ID", f"{order_id}"],
        ["Customer", f"{order.customer.username}"],
        ["Fuel Station", f"{order.station.station_name}"],
        ["Fuel Type", f"{order.fuel_type.fueltype}"],
        ["Quantity", f"{order.quantity} Liter"],
        ["Total Price",  f"{ order.total_price} INR"],
        ["Payment Method", f"{order.payment_method}"],
        ["Payment ID", f"{payment.id}"],
        ["Amount Paid", f"{payment.amount / 100} INR"],
        ["Payment Date", f"{payment.payment_date}"],
    ]

    # Create a table with receipt details
    receipt_table = Table(receipt_details, colWidths=[150, 200])
    receipt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ]))

    # Build PDF document with the title and table
    elements = [title_text, Spacer(1, 20), receipt_table]

    pdf.build(elements)

    buffer.seek(0)
    return buffer



def receipt(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    receipt_pdf = generate_receipt_pdf(order_id)

    # Return the PDF as a downloadable response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{order_id}.pdf"'
    response.write(receipt_pdf.getvalue())

    return response




import webbrowser

def open_google_maps_with_nearby_fuel_bunks(request):
    # Define the location (e.g., latitude and longitude) where you want to find nearby fuel bunks.
    # You can replace these coordinates with your desired location.
    location = "40.7128,-74.0060"
    
    # Create a Google Maps URL with the location and search query for fuel bunks.
    maps_url = f"https://www.google.com/maps/search/fuel+bunk/@{location},15z/data=!3m1!4b1"
    
    # Open the Google Maps URL in the default web browser.
    webbrowser.open(maps_url)

    return render(request, 'map.html')


