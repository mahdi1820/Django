from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lic/', views.lic, name='lic'),
    path('master/', views.mas,name="mas")
]