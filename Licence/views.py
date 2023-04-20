from django.shortcuts import render, redirect ,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import GroupS 
#from .forms import TimeTableForm,StudyTimeForm , StudyTime ,TeacherForm, GroupForm
# Create your views here.

@login_required(login_url = 'login')
def Licence(request):
    return render (request,'Licence/Licence.html')
@login_required(login_url = 'login')
def First_level(request):
    return render (request,'Licence/First_Level.html')
@login_required(login_url = 'login')
def groups(request):
    return render (request,'Licence/create.html')