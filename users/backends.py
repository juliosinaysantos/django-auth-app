from django.contrib.auth.backends import ModelBackend as BaseModelBackend
from django.db.models import Q

from users.models import User


class ModelBackend(BaseModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
