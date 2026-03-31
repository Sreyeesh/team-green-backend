from rest_framework import serializers
from .models import Shop, Barber, Service


class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = ['id', 'name', 'photo_url', 'bio', 'specialties']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'duration_minutes', 'price', 'category']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'slug', 'name', 'description', 'logo_url', 'address', 'phone', 'hours']


class ShopUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo_url', 'address', 'phone', 'hours']
