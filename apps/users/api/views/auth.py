from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random
import string

from apps.users.api.serializers import (
    UserRegistrationSerializer,
    PhoneVerificationSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from apps.users.models import PhoneVerification

User = get_user_model()


def generate_verification_code():
    """Генерирует 6-значный код подтверждения"""
    return ''.join(random.choices(string.digits, k=6))


def send_sms_code(phone_number, code):
    """
    Заглушка для отправки SMS кода
    В реальном проекте здесь будет интеграция с SMS-провайдером
    """
    print(f"SMS отправлен на {phone_number}: Код подтверждения: {code}")
    return True


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    """Регистрация нового пользователя"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Генерируем код подтверждения (временная заглушка - всегда 1111)
        code = "1111"
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Сохраняем код в базе данных
        PhoneVerification.objects.create(
            phone_number=user.phone_number,
            code=code,
            expires_at=expires_at
        )
        
        # Отправляем SMS (заглушка)
        send_sms_code(user.phone_number, code)
        
        return Response({
            'success': True,
            'message': 'Регистрация прошла успешно. Код подтверждения отправлен на ваш номер телефона.',
            'phone_number': user.phone_number
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Ошибка при регистрации',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def phone_verification(request):
    """Подтверждение номера телефона"""
    serializer = PhoneVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        verification = serializer.validated_data['verification']
        phone_number = verification.phone_number
        
        # Отмечаем код как использованный
        verification.is_used = True
        verification.save()
        
        # Подтверждаем номер пользователя
        user = User.objects.get(phone_number=phone_number)
        user.is_phone_verified = True
        user.save()
        
        return Response({
            'success': True,
            'message': 'Регистрация прошла успешно'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Ошибка при подтверждении номера',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Вход в систему"""
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Генерируем JWT токены
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Вход выполнен успешно',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Ошибка при входе в систему',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """Запрос сброса пароля"""
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        
        # Генерируем код подтверждения (временная заглушка - всегда 1111)
        code = "1111"
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Сохраняем код в базе данных
        PhoneVerification.objects.create(
            phone_number=phone_number,
            code=code,
            expires_at=expires_at
        )
        
        # Отправляем SMS (заглушка)
        send_sms_code(phone_number, code)
        
        return Response({
            'success': True,
            'message': 'Код подтверждения отправлен на ваш номер телефона'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Ошибка при запросе сброса пароля',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """Подтверждение сброса пароля"""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    
    if serializer.is_valid():
        verification = serializer.validated_data['verification']
        phone_number = verification.phone_number
        new_password = serializer.validated_data['new_password']
        
        # Отмечаем код как использованный
        verification.is_used = True
        verification.save()
        
        # Обновляем пароль пользователя
        user = User.objects.get(phone_number=phone_number)
        user.set_password(new_password)
        user.save()
        
        return Response({
            'success': True,
            'message': 'Пароль успешно сброшен'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Ошибка при сбросе пароля',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
