from django.urls import path 

from . import views



urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('SignUp/', views.signup, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('admin/logout/', views.Logout, name='logout'),

]