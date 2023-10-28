from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from huliinc_users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_verified= models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    user_information = models.CharField(default="")

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CustomUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    is_verified = serializers.BooleanField(default=False)
    password = serializers.CharField()
