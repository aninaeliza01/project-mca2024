from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.index,name="index"),

    path('login/', views.login_user,name="login"),
    path('logout/', views.logout_user,name="logout"),
    path('registerUser/', views.register_user,name="registerUser"),
    path('profile/', views.customer_Profile,name="profile"),
    path('accounts/profile/', views.userhome,name="userhome"),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),


    path('adminhome/', views.adminhome,name="adminhome"),
    path('update_fuel/<int:fuel_id>/', views.update_fuel, name='update_fuel'),
    path('adminuser/', views.adminuser,name="adminuser"),
    path('adminpump/', views.adminpump,name="adminpump"),
    path('fuel/', views.fuel,name="fuel"),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    
    path('registerPump/', views.register_pump,name="registerPump"),
     

    path('base/', views.base),
    path('adminbase/', views.adminbase),
    path('userhome/', views.userhome,name="userhome"),
    path('pumphome/', views.pumphome,name="pumphome"),
    path('pump/', views.pump,name="pump"),
    path('userBase/', views.userBase,name="userBase"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)