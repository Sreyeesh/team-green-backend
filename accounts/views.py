from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, inline_serializer

from .serializers import RegisterSerializer


class _LoginBodySerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


_TokenResponseSerializer = inline_serializer(
    name='TokenResponse',
    fields={
        'access': serializers.CharField(),
        'refresh': serializers.CharField(),
    },
)


class RegisterView(APIView):
    """POST /api/auth/register"""

    @extend_schema(
        summary='Register a new shop owner',
        request=RegisterSerializer,
        responses={201: _TokenResponseSerializer},
        tags=['Auth'],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """POST /api/auth/login"""

    @extend_schema(
        summary='Login and receive JWT tokens',
        request=_LoginBodySerializer,
        responses={200: _TokenResponseSerializer},
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

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
