from django.urls import path
from . import views

urlpatterns = [
    path('', views.visitor_list, name='visitor_list'),
    path('verify/', views.phone_verification, name='phone_verification'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('form/', views.visitor_form, name='visitor_form'),
    path('success/', views.success, name='success'),
    path('checkout/<int:visitor_id>/', views.checkout_visitor, name='checkout_visitor'),
    path('get-host-details/', views.get_host_details, name='get_host_details'),
    path('approve/', views.approve_visitor, name='approve_visitor'),
    path('reject/', views.reject_visitor, name='reject_visitor'),
    path('schedule/', views.schedule_visitor, name='schedule_visitor'),
    path('block/<int:visitor_id>/', views.block_visitor, name='block_visitor'),
]
