from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer, BookingStatusSerializer
from shops.models import Shop


class BookingCreateView(APIView):
    """POST /api/bookings"""

    @extend_schema(
        summary='Create a new booking',
        request=BookingCreateSerializer,
        responses={201: BookingSerializer},
        tags=['Bookings'],
    )
    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingDetailView(APIView):
    """GET /api/bookings/:id"""

    @extend_schema(
        summary='Get booking details by ID',
        responses={200: BookingSerializer},
        tags=['Bookings'],
    )
    def get(self, request, pk):
        booking = get_object_or_404(Booking, id=pk)
        return Response(BookingSerializer(booking).data)


class BookingConfirmView(APIView):
    """GET /api/bookings/confirm/:code"""

    @extend_schema(
        summary='Look up a booking by confirmation code',
        responses={200: BookingSerializer},
        tags=['Bookings'],
    )
    def get(self, request, code):
        booking = get_object_or_404(Booking, confirmation_code=code.upper())
        return Response(BookingSerializer(booking).data)


class AdminBookingListView(APIView):
    """GET /api/admin/bookings"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List all bookings for your shop',
        parameters=[
            OpenApiParameter('date', OpenApiTypes.DATE, description='Filter by date (YYYY-MM-DD)'),
            OpenApiParameter('status', OpenApiTypes.STR, description='Filter by status: pending | confirmed | cancelled'),
        ],
        responses={200: BookingSerializer(many=True)},
        tags=['Admin — Bookings'],
    )
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
    """PUT /api/admin/bookings/:id"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Update booking status (confirm or cancel)',
        request=BookingStatusSerializer,
        responses={200: BookingSerializer},
        tags=['Admin — Bookings'],
    )
    def put(self, request, pk):
        shop = get_object_or_404(Shop, owner=request.user)
        booking = get_object_or_404(Booking, id=pk, shop=shop)
        serializer = BookingStatusSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(BookingSerializer(booking).data)
