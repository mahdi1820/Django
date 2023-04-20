from django.shortcuts import render ,HttpResponse,redirect
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login ,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.
@login_required(login_url = 'index')
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
            my_user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(my_user)
            return redirect('login')

    return render (request,'home/signup.html')

@login_required(login_url = 'index')
def Logout(request):
    logout(request)
    return redirect('index')  

def index(request):
    return render(request,'home/home.html')


def Teacher_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        
        user = authenticate(request, username = username ,password = pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('Twait')
        else:
            messages.error(request,'Invalid username or password . Please try again.')

    return render (request,'home/TLogin.html')


def Teacher_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request,'You password and conform password are not Same !!!')
        
        else:
            user = User.objects.create_user(username,email,password1)
            user.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return redirect('TLogin')

    return render (request,'home/TSignUp.html')

def Teacher_wait(request):
    return render (request,'home/Teacher_wait.html')