from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.utils.timezone import now

from ..models import Users
from .password import check_password, make_password
from .request_data import request_data
from .token import get_access_user, get_activation_user, generetion_token
from .block import add_ip_blacklist, reset_ip_blacklist


def user_create(request):
    data = request_data(request)
    email = (data.get("email") or "").strip().lower()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    try:
        validate_email(email)
        if not username or len(username) > 100:
            return False

        created_at = now()
        user = Users(
            email=email,
            username=username,
            password="",
            last_login=created_at,
            date_auth=created_at,
            token=generetion_token(),
        )
        validate_password(password, user)
        user.password = make_password(password)
        user.full_clean()
        user.save(force_insert=True)
        return True
    except (ValidationError, IntegrityError):
        return False


def user_delete(request):
    user = get_access_user(request)
    if user is None:
        return False
    user.delete()
    return True


def user_update(request):
    user = get_access_user(request)
    if user is None:
        return False

    data = request_data(request)
    if not check_password(data.get("current_password") or "", user.password):
        return False

    changed_fields = []
    username = data.get("username")
    if username is not None:
        if not isinstance(username, str):
            return False
        username = username.strip()
        if not username or len(username) > 100:
            return False
        user.username = username
        changed_fields.append("username")

    new_password = data.get("new_password")
    if new_password is not None and not isinstance(new_password, str):
        return False
    if new_password:
        try:
            validate_password(new_password, user)
        except ValidationError:
            return False
        user.password = make_password(new_password)
        user.is_active = False
        user.token = generetion_token()
        changed_fields.extend(("password", "is_active", "token"))

    if not changed_fields:
        return False
    user.save(update_fields=changed_fields)
    return True


def verify_login_match(request):
    data = request_data(request)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = Users.objects.filter(email=email).first()

    if user is not None and check_password(password, user.password):
        reset_ip_blacklist(request)
        return True

    add_ip_blacklist(request)
    return False


def connecting_user(request):
    data = request_data(request)
    email = (data.get("email") or "").strip().lower()
    user = Users.objects.filter(email=email).first()
    if user is None or not user.activate:
        return False

    user.is_active = True
    user.last_login = now()
    user.token = generetion_token()
    user.save(update_fields=["is_active", "last_login", "token"])
    return True


def get_user_for_email(request):
    email = (request_data(request).get("email") or "").strip().lower()
    return Users.objects.filter(email=email).first()


def get_user_for_token(request):
    return get_access_user(request)


def disconect_user(request):
    user = get_access_user(request)
    if user is None:
        return False
    user.is_active = False
    user.token = generetion_token()
    user.save(update_fields=["is_active", "token"])
    return True


def return_user_values(request):
    user = get_access_user(request)
    if user is None:
        return None
    return {
        "username": user.username,
        "email": user.email,
        "date_last_login": user.last_login,
    }


def actvation_user(request):
    user = get_activation_user(request.GET.get("token"))
    if user is None:
        return False
    user.activate = True
    user.token = generetion_token()
    user.save(update_fields=["activate", "token"])
    return True


def verify_loged(request):
    return get_access_user(request) is not None
