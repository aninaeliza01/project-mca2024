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
    path('registerUser/', views.register_user,name="registerUser"),
    path('profile/', views.customer_Profile,name="profile"),
    path('changePassword/', views.change_password,name="changePassword"),
    path('accounts/profile/', views.userhome,name="userhome"),
    path('place_order/<int:pump_id>/', views.place_order, name='place_order'),
    path('ordersummary/<int:order_id>/', views.order_summary, name='ordersummary'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('customer_orders/', views.customer_orders, name='customer_orders'),
    path('customer_unorders/', views.customer_unorders, name='customer_unorders'),
    path('pay/<int:order_id>/', views.pay, name='pay'),
    path('download_receipt/<int:order_id>/', views.receipt, name='download_receipt'),
    path('success/<int:order_id>/', views.success, name='success'),

    path('rate_station/<int:station_id>/', views.rate_station, name='rate_station'),
    path('station_detail/<int:station_id>/', views.station_detail, name='station_detail'),
    path('fuel-station/<int:station_id>/', views.fuel_station_detail, name='fuel_station_detail'),

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
    path('adminorder/', views.adminorder,name="adminorder"),
    path('adminratings/', views.ratings_by_station, name='adminratings/'),


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
    path('orders/', views.order,name="orders"),
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('reject_order/<int:order_id>/', views.reject_order, name='reject_order'),
    path('fuelDelivery',views.delivery,name="fuelDelivery"),
    path('mark_delivered/<int:order_id>/', views.mark_delivered, name='mark_delivered'),
    path('station/', views.station_ratings, name='station_ratings'),

    # path('pump/', views.pump,name="pump"),

    path('registerDelivery/', views.register_delivery,name="registerDelivey"),
    path('deliveryBase/', views.deliveryBase,name="deliveryBase"),
    path('deliveryhome/', views.deliveryhome,name="deliveryhome"),
    path('admindelivery/', views.admin_delivery,name="admindelivery"),
    path('delivery-boys/<int:delivery_boy_id>/', views.view_delivery_details, name='view_delivery_details'),
    path('approve_delivery/<int:delivery_boy_id>/', views.approve_delivery, name='approve_delivery'),
    path('reject_delivery/<int:delivery_boy_id>/', views.reject_delivery, name='reject_delivery'),
    path('deliveryprofile/', views.deliveryProfile, name='deliveryprofile'),
    path('deliveryMap/', views.deliveryMap,name="deliveryMap"),

    path('userBase/', views.userBase,name="userBase"),


    path('contact/',views.contact,name="contact"),
    path('contact1/',views.contact1,name="contact1"),
    path('contact2/',views.contact2,name="contact2"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)