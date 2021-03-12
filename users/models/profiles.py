from django.db import models
from django.utils import timezone

from users.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)

    def __str__(self):
        return f'@{self.user.username}'

    def save(self, *args, **kwargs):
        self.user.updated_at = timezone.now()
        self.user.save()
        super().save(*args, **kwargs)
