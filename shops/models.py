from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    logo_url = models.URLField(blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    hours = models.JSONField(default=dict)  # { mon: {open, close}, ... }

    def __str__(self):
        return self.name


class Barber(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='barbers')
    name = models.CharField(max_length=200)
    photo_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    specialties = models.JSONField(default=list)  # string[]

    def __str__(self):
        return f"{self.name} @ {self.shop.name}"


class Service(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.shop.name})"
