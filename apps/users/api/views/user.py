from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.api.serializers import (
    RegionSerializer, 
    ProfileSerializer, 
    ProfileUpdateSerializer, 
    PasswordChangeSerializer
)
from apps.users.models import Region


@api_view(['GET'])
@permission_classes([AllowAny])
def region_list(request):
    """Получение списка регионов"""
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, many=True)
    
    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Получение профиля пользователя"""
    serializer = ProfileSerializer(request.user)
    
    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    """Обновление профиля пользователя"""
    serializer = ProfileUpdateSerializer(
        request.user, 
        data=request.data, 
        partial=request.method == 'PATCH',
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Профиль успешно обновлен',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Ошибка при обновлении профиля',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request):
    """Смена пароля пользователя"""
    serializer = PasswordChangeSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Пароль успешно изменен'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Ошибка при смене пароля',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
