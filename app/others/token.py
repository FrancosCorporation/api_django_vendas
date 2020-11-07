from .password import make_password, check_password
from ..models import *


def generetion_token():
    return make_password('nome').replace('pbkdf2_sha256$216000$', '').replace('=', '').replace('$', '').replace('+', '').replace('/', '')


def verify_token_exists(request,method):
    try:
        new_list = request.META['QUERY_STRING'].split('=')
        token = new_list[1].replace('/', '')
        # vericiando se o token existe
        if(method=='active'):
            if((Users.objects.get(token=token))):
                return True
        if(method == 'normal'):
            if(Users.objects.get(token=request.GET.get('token'))):
                return True
        # se nao achar retorna false
    except:
        return False
