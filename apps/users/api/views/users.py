from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.users import (
    RegistrationSerializer,
    ConfirmPhoneSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Placeholder: send OTP here (SMS) and mark phone as unverified in future
        return Response(
            {
                "detail": "Регистрация успешна",
                "next": reverse('users:confirm-phone'),
                "user_id": user.id,
                "phone_number": user.phone_number,
            },
            status=status.HTTP_201_CREATED,
        )


class ConfirmPhoneView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ConfirmPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Регистрация прошла успешно"})


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        user = authenticate(request, username=phone_number, password=password)
        if not user:
            return Response({"detail": "Неверный номер телефона или пароль"}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            "detail": "Вход выполнен успешно",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class PasswordResetRequestView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Stub: pretend to send SMS with code 1111
        return Response({"detail": "Код отправлен"})


class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Пароль успешно сброшен"})


