from django.urls import path


from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.Licence, name='Licence'),
    path('First_level/', views.First_level, name='First_level'),
    path('lice/First_level/create/', views.create_study_time, name='create_study_time'),
    path('create/', views.create_study_time, name='create_study_time'),

]
