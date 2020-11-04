from django.http import JsonResponse
from .models import ip
from requests_toolbelt.utils import dump


def verify_ip(request,qnt, *args ,**kwargs):
    if request.method == "POST":
        ip_adress = request.META.get('REMOTE_ADDR')
       
