from django.urls import path
from apps.users.api.views import (
    user_registration,
    phone_verification,
    login,
    password_reset_request,
    password_reset_confirm,
    region_list,
    profile_view,
    profile_update,
    password_change
)

app_name = 'users'

urlpatterns = [
    # Регистрация и авторизация
    path('register/', user_registration, name='register'),
    path('verify-phone/', phone_verification, name='verify-phone'),
    path('login/', login, name='login'),
    
    # Сброс пароля
    path('password-reset/', password_reset_request, name='password-reset'),
    path('password-reset-confirm/', password_reset_confirm, name='password-reset-confirm'),
    
    # Профиль пользователя
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update, name='profile-update'),
    path('profile/change-password/', password_change, name='password-change'),
    
    # Справочники
    path('regions/', region_list, name='regions'),
]
