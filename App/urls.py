from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns = [

    path('', views.index,name="index"),

    path('login/', views.login_user,name="login"),
    path('logout/', views.logout_user,name="logout"),
    path('registerUser/', views.register_user,name="registerUser"),
    # path('profile/', views.user_profile,name="profile"),


    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),



    path('registerPump/', views.register_pump,name="registerPump"),
     
    path('about/', views.about),
    path('contact/', views.contact),
    # path('Pump/', views.Pump),
    path('base/', views.base),
    path('userhome/', views.userhome,name="userhome"),
    path('pumphome/', views.pumphome,name="pumphome"),
    
]