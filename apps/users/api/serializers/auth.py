from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from apps.users.models import User, PhoneVerification, Region
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор для регионов"""
    class Meta:
        model = Region
        fields = ['id', 'name', 'code']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    terms_accepted = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 
            'region', 'password', 'password_confirm', 'terms_accepted'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        
        if not attrs['terms_accepted']:
            raise serializers.ValidationError("Необходимо принять условия использования")
        
        return attrs
    
    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона уже существует")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            region=validated_data.get('region'),
            terms_accepted=validated_data['terms_accepted'],
            password=password
        )
        return user


class PhoneVerificationSerializer(serializers.Serializer):
    """Сериализатор для подтверждения номера телефона"""
    phone_number = serializers.CharField(max_length=17)
    code = serializers.CharField(max_length=6)
    
    def validate_code(self, value):
        # Временная заглушка: только код 1111 считается правильным
        if value != '1111':
            raise serializers.ValidationError("Неверный код подтверждения")
        return value
    
    def validate(self, attrs):
        phone_number = attrs['phone_number']
        code = attrs['code']
        
        # Проверяем, есть ли активный код для этого номера
        verification = PhoneVerification.objects.filter(
            phone_number=phone_number,
            code=code,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()
        
        if not verification:
            raise serializers.ValidationError("Неверный или истекший код подтверждения")
        
        attrs['verification'] = verification
        return attrs


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа в систему"""
    phone_number = serializers.CharField(max_length=17)
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        phone_number = attrs['phone_number']
        password = attrs['password']
        
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError("Неверный номер телефона или пароль")
        
        if not user.is_phone_verified:
            raise serializers.ValidationError("Номер телефона не подтвержден")
        
        attrs['user'] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса сброса пароля"""
    phone_number = serializers.CharField(max_length=17)
    
    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона не найден")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Сериализатор для подтверждения сброса пароля"""
    phone_number = serializers.CharField(max_length=17)
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate_code(self, value):
        # Временная заглушка: только код 1111 считается правильным
        if value != '1111':
            raise serializers.ValidationError("Неверный код подтверждения")
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        
        phone_number = attrs['phone_number']
        code = attrs['code']
        
        # Проверяем, есть ли активный код для этого номера
        verification = PhoneVerification.objects.filter(
            phone_number=phone_number,
            code=code,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()
        
        if not verification:
            raise serializers.ValidationError("Неверный или истекший код подтверждения")
        
        attrs['verification'] = verification
        return attrs
