import secrets
from datetime import timedelta

from django.utils.timezone import now

from ..models import Users
from .request_data import bearer_token


ACCESS_TOKEN_TTL = timedelta(hours=1)
ACTIVATION_TOKEN_TTL = timedelta(hours=24)


def generetion_token():
    """Generate an unguessable token; the misspelled name is kept for compatibility."""
    return secrets.token_urlsafe(48)


def get_access_user(request):
    token = bearer_token(request)
    if not token or len(token) > 164:
        return None

    try:
        user = Users.objects.get(token=token, is_active=True, activate=True)
    except Users.DoesNotExist:
        return None

    age = now() - user.last_login
    if age < timedelta(0) or age > ACCESS_TOKEN_TTL:
        if user.is_active:
            user.is_active = False
            user.save(update_fields=["is_active"])
        return None
    return user


def get_activation_user(token):
    if not token or len(token) > 164:
        return None
    try:
        user = Users.objects.get(token=token, activate=False)
    except Users.DoesNotExist:
        return None

    age = now() - user.date_auth
    if age < timedelta(0) or age > ACTIVATION_TOKEN_TTL:
        return None
    return user


def verify_token_exists(request, method):
    if method == "active":
        return get_activation_user(request.GET.get("token")) is not None
    if method == "normal":
        return get_access_user(request) is not None
    return False
