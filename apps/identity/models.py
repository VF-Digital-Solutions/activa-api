from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import UUIDModel


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
