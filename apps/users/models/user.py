from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User"""
    
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone_number, password, **extra_fields)


class Region(models.Model):
    """Модель для хранения регионов"""
    name = models.CharField(max_length=100, verbose_name="Название региона")
    code = models.CharField(max_length=10, unique=True, verbose_name="Код региона")
    
    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    """Кастомная модель пользователя"""
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        unique=True,
        verbose_name="Номер телефона"
    )
    region = models.ForeignKey(
        Region, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Регион"
    )
    is_phone_verified = models.BooleanField(default=False, verbose_name="Номер подтвержден")
    terms_accepted = models.BooleanField(default=False, verbose_name="Согласие с условиями")
    
    # Убираем username, используем phone_number как основное поле для входа
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"


class PhoneVerification(models.Model):
    """Модель для хранения кодов подтверждения номера телефона"""
    phone_number = models.CharField(max_length=17, verbose_name="Номер телефона")
    code = models.CharField(max_length=6, verbose_name="Код подтверждения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    is_used = models.BooleanField(default=False, verbose_name="Использован")
    expires_at = models.DateTimeField(verbose_name="Истекает")
    
    class Meta:
        verbose_name = "Подтверждение номера"
        verbose_name_plural = "Подтверждения номеров"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.phone_number} - {self.code}"
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
