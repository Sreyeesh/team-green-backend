import uuid
from django.db import models
from shops.models import Shop, Barber, Service


def _short_code():
    return uuid.uuid4().hex[:8].upper()


class Booking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='bookings')
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    datetime = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    confirmation_code = models.CharField(max_length=8, unique=True, default=_short_code, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} with {self.barber.name} on {self.datetime}"
