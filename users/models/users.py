from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class User(AbstractUser, BaseModel):

    username = models.CharField('username', max_length=50, unique=True)
    email = models.EmailField('email address', unique=True)

    # This fields will be in the Profile Model.
    first_name = None
    last_name = None
    date_joined = None

    email_verified_at = models.DateTimeField('email verified at', null=True, blank=True)
    email_verification_token = models.CharField('email verification token', max_length=32, blank=True)

    def __str__(self):
        return f'@{self.username}'

    def get_full_name(self):
        return f'{self.profile.first_name} {self.profile.last_name}'

    def get_short_name(self):
        return self.username
