from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from catalog.models import NULLABLE
from django.utils.crypto import get_random_string


class User(AbstractUser):
    username = None
    email = models.EmailField(_("почта"), max_length=254, unique=True)
    is_active = models.BooleanField(
        _("верификация почты"), default=False)
    email_verification_token = models.CharField(
        _("токен для подтверждения почты"), max_length=30, unique=True)

    phone = models.CharField(_("телефон"), max_length=35, **NULLABLE)
    avatar = models.ImageField(_("аватар"), upload_to='users/', **NULLABLE)
    country = models.CharField(_("страна"), max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []



    @staticmethod
    def generate_token(check_additional=False):
        token = get_random_string(length=30)
        try:
            while User.objects.get(email_verification_token=token) or User.objects.get(reset_password_token=token) or token != check_additional:
                token = get_random_string(length=30)
        finally:
            return token

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.email_verification_token = self.generate_token()
            self.reset_password_token = self.generate_token(
                self.email_verification_token)
        return super().save(*args, **kwargs)
