from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.index,name="index"),

    path('login/', views.login_user,name="login"),
    path('logout/', views.logout_user,name="logout"),

    path('userhome/', views.userhome,name="userhome"),
    path('profile/', views.customer_Profile,name="profile"),
    path('changePassword/', views.change_password,name="changePassword"),
    path('accounts/profile/', views.userhome,name="userhome"),
    path('place_order/<int:pump_id>/', views.place_order, name='place_order'),
    path('ordersummary/<int:order_id>/', views.order_summary, name='ordersummary'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('customer_orders/', views.customer_orders, name='customer_orders'),

    path('adminhome/', views.adminhome,name="adminhome"),
    path('update_fuel/<int:fuel_id>/', views.update_fuel, name='update_fuel'),
    path('delete_fuel/<int:fuel_id>/', views.delete_fuel, name='delete_fuel'),
    path('adminuser/', views.adminuser,name="adminuser"),
    path('block_unblock_user/<int:user_id>/', views.block_unblock_user, name='block_unblock_user'),
    path('adminpump/', views.adminpump,name="adminpump"),
    path('fuel/', views.fuel,name="fuel"),
    path('location/', views.location,name="location"),
    path('update_location/<int:location_id>/', views.update_location, name='update_location'),
    path('delete_location/<int:location_id>/', views.delete_location, name='delete_location'),


    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    
    path('registerPump/', views.register_pump,name="registerPump"),
    path('FuelProfile/', views.fuel_station_profile, name='fuel_profile'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
     

    path('base/', views.base),
    path('adminbase/', views.adminbase),

    path('pumphome/', views.pumphome,name="pumphome"),
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('reject_order/<int:order_id>/', views.reject_order, name='reject_order'),
    # path('pump/', views.pump,name="pump"),

    
    path('userBase/', views.userBase,name="userBase"),


    path('map/', views.open_google_maps_with_nearby_fuel_bunks,name="map"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)