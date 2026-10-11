from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.urls import reverse

from app.models import Users
from .request_data import request_data


def validador_email_correct(request):
    email = (request_data(request).get("email") or "").strip()
    if len(email) > 100:
        return False
    try:
        validate_email(email)
    except ValidationError:
        return False
    return True


def verificador_email_db(request):
    email = (request_data(request).get("email") or "").strip().lower()
    return Users.objects.filter(email=email).exists()


def send_email(email, username, token, request):
    path = reverse("account-activation")
    base_url = settings.PUBLIC_BASE_URL.rstrip("/")
    if not base_url:
        base_url = request.build_absolute_uri("/").rstrip("/")
    query = urlencode({"token": token})
    activation_url = f"{base_url}{path}?{query}"
    message = EmailMessage(
        subject="Ativação de conta",
        body=(
            f"Olá, {username}! Use o link abaixo para ativar sua conta. "
            "O link expira em 24 horas e pode ser usado uma única vez.\n\n"
            f"{activation_url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    message.send(fail_silently=False)


def verify_email_existy(request):
    return verificador_email_db(request)
