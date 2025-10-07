from django.urls import path
from .views import (
    RegisterView,
    ConfirmPhoneView,
    LoginView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)


app_name = 'users'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-phone/', ConfirmPhoneView.as_view(), name='confirm-phone'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]


