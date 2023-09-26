
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('registerUser/', views.register),
    path('about/', views.about),
    path('contact/', views.contact),
    path('Pump/', views.Pump),
    path('base/', views.base),
    path('userhome/', views.userhome),
    
]