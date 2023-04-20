from django.urls import path


from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.Licence, name='Licence'),
    path('First_level/', views.First_level, name='First_level'),
    path('First_level/groups', views.groups, name='groups'),

]
