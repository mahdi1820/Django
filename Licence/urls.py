from django.urls import path

from . import views

urlpatterns = [
    path('Licence/', views.Licence, name='Licence'),
]