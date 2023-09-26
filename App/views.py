from django.shortcuts import render,redirect

from django.contrib import messages
from django.contrib.auth import authenticate ,login ,logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    # if request.method == 'POST':
    #     # Process the registration form data
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     phone = request.POST['phone']
    #     password = request.POST['pass']
    #     confirm_password = request.POST['cpass']
    #     role = CustomUser.PATIENT  # Set the user role as needed

    #     if username and email and phone and password and role:
    #         if CustomUser.objects.filter(email=email).exists():
    #             error_message = "Email is already registered."
    #         elif password != confirm_password:
    #             error_message = "Passwords do not match."
    #         else:
    #             # Create a new user
    #             user = CustomUser(username=username, email=email, phone=phone, role=role)
    #             user.set_password(password)  # Set the password securely
    #             user.save()
    #             # You may want to activate the user's account here or send a confirmation email
    #             return redirect('login')
    #     else:
    #         error_message = "All fields are required."

    #     return render(request, 'registerUser.html', {'error_message': error_message})

    # Handle GET request to render the registration form
    return render(request, 'registerUser.html')

def login(request):
    return render(request, 'login.html')
def signout(request):
    logout(request)
    messages.success(request,())
    return  redirect('index')
def userhome(request):
    return render(request, 'userhome.html')
    
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def Pump(request):
    return render(request, 'Pump.html')
def base(request):
    return render(request, 'base.html')