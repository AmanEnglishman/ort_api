from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    region = serializers.ChoiceField(choices=User.REGION_CHOICES)
    phone_number = serializers.CharField(
        max_length=20,
        validators=[
            RegexValidator(r"^[0-9+\-()\s]{7,20}$", message="Некорректный номер телефона"),
        ],
    )
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    accept_terms = serializers.BooleanField(write_only=True)

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером уже существует")
        return value

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password_confirm"):
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})
        if not attrs.get("accept_terms"):
            raise serializers.ValidationError({"accept_terms": "Необходимо согласие с условиями"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm", None)
        validated_data.pop("accept_terms", None)
        password = validated_data.pop("password")
        user: User = User.objects.create_user(password=password, **validated_data)
        return user


class ConfirmPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=10)

    def validate(self, attrs):
        if attrs.get("code") != "1111":
            raise serializers.ValidationError({"code": "Неверный код подтверждения"})
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером не найден")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=10)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs.get("code") != "1111":
            raise serializers.ValidationError({"code": "Неверный код подтверждения"})
        if attrs.get("new_password") != attrs.get("new_password_confirm"):
            raise serializers.ValidationError({"new_password_confirm": "Пароли не совпадают"})
        return attrs

    def save(self):
        phone_number = self.validated_data["phone_number"]
        new_password = self.validated_data["new_password"]
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"phone_number": "Пользователь не найден"})
        user.set_password(new_password)
        user.save()
        return user


