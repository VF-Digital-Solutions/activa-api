from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import choices
from apps.core.models import TimeStampedModel, UUIDModel


class User(AbstractUser, UUIDModel):
    """
    Usuario base del sistema
    Usa email como campo de login en lugar de username
    """

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    preferred_language = models.CharField(max_length=10, default="es")
    timezone = models.CharField(max_length=50, default="UTC")
    notification_preferences = models.JSONField(default=dict)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "identity_user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email


class UserDevice(TimeStampedModel):

    class Platform(models.TextChoices):
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"
        WEB = "WEB", "Web"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    device_token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=10, choices=Platform.choices)
    is_active = models.BooleanField(default=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "identity_user_device"
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

    def __str__(self):
        return f"{self.user.email} - {self.platform}"
