
from django.urls import path
from . import views
urlpatterns = [

    path('', views.index,name="index"),

    path('login/', views.login_user,name="login"),
    path('userhome/logout', views.logout_user,name="logout"),
    path('registerUser/', views.register_user,name="registerUser"),

    path('registerPump/', views.register_pump,name="registerPump"),
     
    path('about/', views.about),
    path('contact/', views.contact),
    path('Pump/', views.Pump),
    path('base/', views.base),
    path('userhome/', views.userhome,name="userhome"),
    
]