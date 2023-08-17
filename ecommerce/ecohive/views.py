from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        Cpassword = request.POST.get('cpwd')

        if password == Cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email,password=password)
                user.save()
                messages.info(request, "Registered")
                return redirect('login.html')  # Redirect to login page
        else:
            messages.info(request, "Passwords do not match")
            return redirect('register')
    return render(request, 'register.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#     if username == 'legaladvisor' and password == 'Advisor@2023':
#         if user is not None:
#             auth_login(request, user)
#             return render(request, 'dashlegal.html') 
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth_login(request, user)
#             request.session['user_id'] = user.id
#             request.session['username'] = user.username
#             return redirect('index')  # Replace with your desired URL
#         else:
#             messages.error(request, "Invalid credentials")
#             return redirect('login')
#     else:
#         return render(request, 'login.html')
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the provided credentials match the legal advisor's credentials
        if username == 'legaladvisor' and password == 'Advisor@2023':
            # Authenticate and log in the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('dashlegal.html')  # Redirect legal advisor to index.html
            
            messages.error(request, "Invalid credentials")
            return redirect('login')
        else:
            # Authenticate other users
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('index')  # Redirect other users to index.html
            
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')


def sellerreg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        Cpassword = request.POST.get('cpwd')

        if password == Cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email,password=password)
                user.save()
                messages.info(request, "Registered")
                return redirect('login')  # Redirect to login page
        else:
            messages.info(request, "Passwords do not match")
            return redirect('register')
    return render(request, 'register.html')

def loggout(request):
    print('Logged Out')
    logout(request)
    if 'username' in request.session:
        del request.session['username']
        request.session.clear()
    return redirect('index')

def check_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})
def dashlegal(request):
    return render(request, 'dashlegal.html')
def dashseller(request):
    return render(request, 'dashseller.html')