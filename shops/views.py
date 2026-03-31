import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Shop, Barber, Service
from .serializers import ShopSerializer, BarberSerializer, ServiceSerializer, ShopUpdateSerializer
from bookings.models import Booking


# ─── Public Views ─────────────────────────────────────────────────────────────

class ShopDetailView(APIView):
    """GET /api/shops/:slug"""

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        return Response(ShopSerializer(shop).data)


class ShopBarbersView(APIView):
    """GET /api/shops/:slug/barbers"""

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        return Response(BarberSerializer(shop.barbers.all(), many=True).data)


class ShopServicesView(APIView):
    """GET /api/shops/:slug/services"""

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        return Response(ServiceSerializer(shop.services.all(), many=True).data)


class ShopAvailabilityView(APIView):
    """GET /api/shops/:slug/availability?barber_id=&service_id=&date=YYYY-MM-DD"""

    def get(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug)
        barber_id = request.query_params.get('barber_id')
        service_id = request.query_params.get('service_id')
        date_str = request.query_params.get('date')

        if not all([barber_id, service_id, date_str]):
            return Response(
                {'error': 'barber_id, service_id, and date are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        barber = get_object_or_404(Barber, id=barber_id, shop=shop)
        service = get_object_or_404(Service, id=service_id, shop=shop)

        try:
            date = datetime.date.fromisoformat(date_str)
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        slot_duration = datetime.timedelta(minutes=service.duration_minutes)

        # Use shop hours for this day, fall back to 09:00–18:00
        day_name = date.strftime('%a').lower()  # mon, tue, wed...
        day_hours = shop.hours.get(day_name, {})
        open_str = day_hours.get('open', '09:00')
        close_str = day_hours.get('close', '18:00')

        try:
            open_time = datetime.time.fromisoformat(open_str)
            close_time = datetime.time.fromisoformat(close_str)
        except ValueError:
            open_time = datetime.time(9, 0)
            close_time = datetime.time(18, 0)

        day_start = datetime.datetime.combine(date, open_time)
        day_end = datetime.datetime.combine(date, close_time)

        existing = Booking.objects.filter(
            barber=barber,
            datetime__date=date,
            status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED],
        )
        booked_ranges = [
            (b.datetime.replace(tzinfo=None), (b.datetime + datetime.timedelta(minutes=b.duration_minutes)).replace(tzinfo=None))
            for b in existing
        ]

        slots = []
        current = day_start
        while current + slot_duration <= day_end:
            slot_end = current + slot_duration
            is_available = not any(
                start < slot_end and end > current
                for start, end in booked_ranges
            )
            slots.append({
                'datetime': current.isoformat(),
                'barber_id': barber.id,
                'available': is_available,
            })
            current += slot_duration

        return Response(slots)


# ─── Admin Views ───────────────────────────────────────────────────────────────

class AdminShopView(APIView):
    """GET/PUT /api/admin/shop"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shop = get_object_or_404(Shop, owner=request.user)
        return Response(ShopSerializer(shop).data)

    def put(self, request):
        shop = get_object_or_404(Shop, owner=request.user)
        serializer = ShopUpdateSerializer(shop, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ShopSerializer(shop).data)


class AdminBarberListView(APIView):
    """GET/POST /api/admin/barbers"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shop = get_object_or_404(Shop, owner=request.user)
        return Response(BarberSerializer(shop.barbers.all(), many=True).data)

    def post(self, request):
        shop = get_object_or_404(Shop, owner=request.user)
        serializer = BarberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(shop=shop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminBarberDetailView(APIView):
    """PUT/DELETE /api/admin/barbers/:id"""
    permission_classes = [IsAuthenticated]

    def _get_barber(self, request, pk):
        shop = get_object_or_404(Shop, owner=request.user)
        return get_object_or_404(Barber, id=pk, shop=shop)

    def put(self, request, pk):
        barber = self._get_barber(request, pk)
        serializer = BarberSerializer(barber, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self._get_barber(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminServiceListView(APIView):
    """GET/POST /api/admin/services"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shop = get_object_or_404(Shop, owner=request.user)
        return Response(ServiceSerializer(shop.services.all(), many=True).data)

    def post(self, request):
        shop = get_object_or_404(Shop, owner=request.user)
        serializer = ServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(shop=shop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminServiceDetailView(APIView):
    """PUT/DELETE /api/admin/services/:id"""
    permission_classes = [IsAuthenticated]

    def _get_service(self, request, pk):
        shop = get_object_or_404(Shop, owner=request.user)
        return get_object_or_404(Service, id=pk, shop=shop)

    def put(self, request, pk):
        service = self._get_service(request, pk)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self._get_service(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
