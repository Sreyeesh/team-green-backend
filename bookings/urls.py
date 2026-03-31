from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('confirm/<str:code>/', views.BookingConfirmView.as_view(), name='booking-confirm'),

    # Admin
    path('admin/', views.AdminBookingListView.as_view(), name='admin-bookings'),
    path('admin/<int:pk>/', views.AdminBookingDetailView.as_view(), name='admin-booking-detail'),
]
