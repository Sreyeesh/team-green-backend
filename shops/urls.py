from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('<slug:slug>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('<slug:slug>/barbers/', views.ShopBarbersView.as_view(), name='shop-barbers'),
    path('<slug:slug>/services/', views.ShopServicesView.as_view(), name='shop-services'),
    path('<slug:slug>/availability/', views.ShopAvailabilityView.as_view(), name='shop-availability'),

    # Admin
    path('admin/shop/', views.AdminShopView.as_view(), name='admin-shop'),
    path('admin/barbers/', views.AdminBarberListView.as_view(), name='admin-barbers'),
    path('admin/barbers/<int:pk>/', views.AdminBarberDetailView.as_view(), name='admin-barber-detail'),
    path('admin/services/', views.AdminServiceListView.as_view(), name='admin-services'),
    path('admin/services/<int:pk>/', views.AdminServiceDetailView.as_view(), name='admin-service-detail'),
]
