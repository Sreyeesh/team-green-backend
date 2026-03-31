from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('<slug:slug>/barbers/', views.ShopBarbersView.as_view(), name='shop-barbers'),
    path('<slug:slug>/services/', views.ShopServicesView.as_view(), name='shop-services'),
    path('<slug:slug>/availability/', views.ShopAvailabilityView.as_view(), name='shop-availability'),
]
