from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    is_content_manager = models.BooleanField(default=False, verbose_name='контент-менеджер')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
