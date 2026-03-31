from django.urls import path
from shops.views import (
    AdminShopView,
    AdminBarberListView, AdminBarberDetailView,
    AdminServiceListView, AdminServiceDetailView,
)
from bookings.views import AdminBookingListView, AdminBookingDetailView

urlpatterns = [
    path('shop/', AdminShopView.as_view(), name='admin-shop'),
    path('barbers/', AdminBarberListView.as_view(), name='admin-barbers'),
    path('barbers/<int:pk>/', AdminBarberDetailView.as_view(), name='admin-barber-detail'),
    path('services/', AdminServiceListView.as_view(), name='admin-services'),
    path('services/<int:pk>/', AdminServiceDetailView.as_view(), name='admin-service-detail'),
    path('bookings/', AdminBookingListView.as_view(), name='admin-bookings'),
    path('bookings/<int:pk>/', AdminBookingDetailView.as_view(), name='admin-booking-detail'),
]
