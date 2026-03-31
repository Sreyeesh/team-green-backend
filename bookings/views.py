from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer, BookingStatusSerializer
from shops.models import Shop


class BookingCreateView(APIView):
    """POST /api/bookings"""

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingDetailView(APIView):
    """GET /api/bookings/:id"""

    def get(self, request, pk):
        booking = get_object_or_404(Booking, id=pk)
        return Response(BookingSerializer(booking).data)


class BookingConfirmView(APIView):
    """GET /api/bookings/confirm/:code — guest lookup by confirmation code"""

    def get(self, request, code):
        booking = get_object_or_404(Booking, confirmation_code=code.upper())
        return Response(BookingSerializer(booking).data)


class AdminBookingListView(APIView):
    """GET /api/admin/bookings?date=YYYY-MM-DD&status="""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shop = get_object_or_404(Shop, owner=request.user)
        qs = Booking.objects.filter(shop=shop).order_by('datetime')

        date_str = request.query_params.get('date')
        if date_str:
            qs = qs.filter(datetime__date=date_str)

        booking_status = request.query_params.get('status')
        if booking_status:
            qs = qs.filter(status=booking_status)

        return Response(BookingSerializer(qs, many=True).data)


class AdminBookingDetailView(APIView):
    """PUT /api/admin/bookings/:id  (update status)"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        shop = get_object_or_404(Shop, owner=request.user)
        booking = get_object_or_404(Booking, id=pk, shop=shop)
        serializer = BookingStatusSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(BookingSerializer(booking).data)
