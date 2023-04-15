from django.shortcuts import render ,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login ,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = 'login')
def home(request):
    return render (request,'home/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        
        user = authenticate(request, username = username ,password = pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password . Please try again.')

    return render (request,'home/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request,'You password and conform password are not Same !!!')
        
        else:
            my_user = User.objects.create_user(username,email,password1)
            #my_user  = SignUp (uname = username ,email = email ,password1 = password1)
            my_user.save()

            return redirect('login')

    return render (request,'home/signup.html')
@login_required(login_url = 'login')
def Logout(request):
    logout(request)
    return redirect('login')  