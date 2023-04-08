from django.shortcuts import render

# Create your views here.

def home(request):
    return render (request,'calc/index.html')

def lic(request):
    return render (request,'calc/lic.html')

def master(request):
    return render (request,'calc/mas.html')    