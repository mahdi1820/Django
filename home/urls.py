from django.urls import path 

from . import views



urlpatterns = [
    path('home/', views.home, name='home'),
    path('Admin_Login', views.login, name='login'),
    path('Admin_SignUp/', views.signup, name='signup'),
    path('Teacher_Login', views.Teacher_login, name='TLogin'),
    path('Teacher_wait', views.Teacher_wait, name='Twait'),
    path('Teacher_SignUp/', views.Teacher_signup, name='TSignup'),
    path('admin/logout/', views.Logout, name='admin_logout'),
    path('', views.index, name='index'),
    
]