from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    registration_key = models.CharField(max_length=100, verbose_name='Регистрационный ключ')
    is_active = models.BooleanField(default=False, verbose_name='Флаг верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
