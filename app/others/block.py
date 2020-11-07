from django.utils.timezone import now
from app.models import Ip
from app.serializers import IpSerializers

def verify_ip(request, duration):
    ip_address = request.META.get('REMOTE_ADDR')
    # verficando se o ip existe se exitir passa aqui
    if(verify_ip_exist(request) is False):
        data = {'ip_address': ip_address, 'count': 0, 'date_last_try': now()}
        ip_serializado = IpSerializers(data=data)
        if(ip_serializado.is_valid()):
            ip_serializado.save()
            return True
    # se ele existir e for maior que count 5 ele nao pode passar
    else:
        ip = Ip.objects.get(ip_address=request.META.get('REMOTE_ADDR'))
        if((ip.count <= 5)):
            return True
        else:
            new_time = now() - ip.date_last_try
            if((new_time.seconds/3600) >= (duration/60)):#duration em minutos
                data = {'ip_address': ip_address,
                        'count': 1, 'date_last_try': now()}
                ip_serializado = IpSerializers(ip, data=data)
                if(ip_serializado.is_valid()):
                    ip_serializado.save()
                return True
            else:
                return False


def verify_ip_exist(request):
    try:
        if(Ip.objects.get(ip_address=request.META.get('REMOTE_ADDR'))):
            return True
        else:
            return False
    except:
        return False


def add_ip_blacklist(request):
    ip_address = request.META.get('REMOTE_ADDR')
    ip = Ip.objects.get(ip_address=request.META.get('REMOTE_ADDR'))
    data = {'ip_address': ip_address,
            'count': ip.count+1, 'date_last_try': now()}
    ip_serializado = IpSerializers(ip, data=data)
    if(ip_serializado.is_valid()):
        ip_serializado.save()
