from rest_framework import serializers
from .models import Booking
from shops.serializers import BarberSerializer, ServiceSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'barber', 'service', 'datetime',
            'customer_name', 'customer_email', 'customer_phone',
        ]

    def validate(self, data):
        barber = data['barber']
        service = data['service']
        dt = data['datetime']

        # Ensure barber and service belong to the same shop
        if barber.shop != service.shop:
            raise serializers.ValidationError("Barber and service must belong to the same shop.")

        # Check for conflicting bookings
        duration = service.duration_minutes
        from django.utils import timezone
        import datetime
        slot_end = dt + datetime.timedelta(minutes=duration)

        conflicts = Booking.objects.filter(
            barber=barber,
            status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED],
        ).exclude(datetime__gte=slot_end)

        for booking in conflicts:
            existing_end = booking.datetime + datetime.timedelta(minutes=booking.duration_minutes)
            if booking.datetime < slot_end and existing_end > dt:
                raise serializers.ValidationError("This time slot is already booked.")

        return data

    def create(self, validated_data):
        service = validated_data['service']
        barber = validated_data['barber']
        validated_data['shop'] = barber.shop
        validated_data['duration_minutes'] = service.duration_minutes
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    barber = BarberSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'confirmation_code', 'shop', 'barber', 'service', 'datetime',
            'duration_minutes', 'customer_name', 'customer_email', 'customer_phone',
            'status', 'created_at',
        ]


class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']
