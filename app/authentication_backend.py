# authentication.py
from django.contrib.auth.backends import BaseBackend
from .models import Users

class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        user = (
            Users.objects.filter(email=identifier).first() or
            Users.objects.filter(phone=identifier).first()
        )
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
