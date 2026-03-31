from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'barber', 'service', 'datetime', 'status', 'confirmation_code']
    list_filter = ['status', 'barber', 'datetime']
    search_fields = ['customer_name', 'customer_email', 'confirmation_code']
    readonly_fields = ['confirmation_code', 'created_at']
    ordering = ['-datetime']
