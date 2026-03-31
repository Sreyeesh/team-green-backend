from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('confirm/<str:code>/', views.BookingConfirmView.as_view(), name='booking-confirm'),
]
