from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login ,logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register_user(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['pass']
    
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

def login_user(request):
    if request.method =='POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/userhome')
        else:
            messages.success(request,("there was an error"))
            return redirect('/login')
    else:
        return render(request, 'login.html')
def logout_user(request):
    logout(request)
    messages.success(request,("Logged out"))
    return  redirect('userhome')
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