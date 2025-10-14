from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.users.models import User, Region


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 
            'region', 'region_name', 'is_phone_verified', 'date_joined'
        ]
        read_only_fields = ['id', 'is_phone_verified', 'date_joined']


class RegionSerializer(serializers.ModelSerializer):
    """Сериализатор для регионов"""
    class Meta:
        model = Region
        fields = ['id', 'name', 'code']


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения профиля пользователя"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'phone_number', 
            'region', 'region_name', 'is_phone_verified', 'date_joined'
        ]
        read_only_fields = ['id', 'phone_number', 'is_phone_verified', 'date_joined']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля пользователя"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'region', 'region_name'
        ]
    
    def update(self, instance, validated_data):
        # Обновляем только переданные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """Сериализатор для смены пароля"""
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Текущий пароль неверен")
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Новые пароли не совпадают")
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
