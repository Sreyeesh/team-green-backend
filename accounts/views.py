from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, inline_serializer

from .serializers import RegisterSerializer
from shops.models import Shop
from shops.serializers import ShopSerializer


class _LoginBodySerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


_AuthResponseSerializer = inline_serializer(
    name='AuthResponse',
    fields={
        'token': serializers.CharField(),
        'refresh': serializers.CharField(),
        'shop': ShopSerializer(),
    },
)


def _auth_response(user, status_code):
    refresh = RefreshToken.for_user(user)
    shop = Shop.objects.filter(owner=user).first()
    return Response({
        'token': str(refresh.access_token),
        'refresh': str(refresh),
        'shop': ShopSerializer(shop).data if shop else None,
    }, status=status_code)


class RegisterView(APIView):
    """POST /api/auth/register/"""

    @extend_schema(
        summary='Register a new shop owner',
        request=RegisterSerializer,
        responses={201: _AuthResponseSerializer},
        tags=['Auth'],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return _auth_response(user, status.HTTP_201_CREATED)


class LoginView(APIView):
    """POST /api/auth/login/"""

    @extend_schema(
        summary='Login and receive token + shop details',
        request=_LoginBodySerializer,
        responses={200: _AuthResponseSerializer},
        tags=['Auth'],
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return _auth_response(user, status.HTTP_200_OK)
