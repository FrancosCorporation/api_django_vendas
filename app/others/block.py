from datetime import timedelta

from django.db import transaction
from django.utils.timezone import now

from ..models import Ip


MAX_FAILED_LOGINS = 5


def _client_ip(request):
    # Do not trust X-Forwarded-For here; REMOTE_ADDR is supplied by the server.
    return request.META.get("REMOTE_ADDR")


def verify_ip(request, duration):
    ip_address = _client_ip(request)
    if not ip_address:
        return False

    current_time = now()
    cooldown = timedelta(minutes=duration)
    with transaction.atomic():
        record, _ = Ip.objects.select_for_update().get_or_create(
            ip_address=ip_address,
            defaults={"count": 0, "date_last_try": current_time},
        )
        if current_time - record.date_last_try >= cooldown:
            record.count = 0
            record.date_last_try = current_time
            record.save(update_fields=["count", "date_last_try"])
        return record.count < MAX_FAILED_LOGINS


def add_ip_blacklist(request):
    ip_address = _client_ip(request)
    if not ip_address:
        return

    current_time = now()
    cooldown = timedelta(minutes=2)
    with transaction.atomic():
        record, _ = Ip.objects.select_for_update().get_or_create(
            ip_address=ip_address,
            defaults={"count": 0, "date_last_try": current_time},
        )
        if current_time - record.date_last_try >= cooldown:
            record.count = 1
        else:
            record.count += 1
        record.date_last_try = current_time
        record.save(update_fields=["count", "date_last_try"])


def reset_ip_blacklist(request):
    ip_address = _client_ip(request)
    if ip_address:
        Ip.objects.filter(ip_address=ip_address).update(count=0, date_last_try=now())
