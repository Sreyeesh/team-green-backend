from django.contrib import admin
from .models import Shop, Barber, Service


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'phone', 'owner']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop']
    list_filter = ['shop']
    search_fields = ['name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'category', 'duration_minutes', 'price']
    list_filter = ['shop', 'category']
    search_fields = ['name']
