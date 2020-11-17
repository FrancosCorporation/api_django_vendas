import hashlib
from django.contrib.auth.hashers import make_password
from ..models import *


def generetion_token():
    return hash_string(make_password('nome').replace('pbkdf2_sha256$216000$', '').replace('=', '').replace('$', '').replace('+', '').replace('/', ''))

def verify_token_exists(request, method):
    try:
        new_list = request.META['QUERY_STRING'].split('=')
        token = new_list[1].replace('/', '')
        # vericiando se o token existe
        if(method == 'activation'):
            if((Users.objects.get(token=token))):
                return True
        if(method == 'normal'):
            if(Users.objects.get(token=request.GET.get('token'))):
                return True
        # se nao achar retorna false
        else:
            return False
    except:
        return False

def hash_string(string):
    return hashlib.sha3_512(string.encode()).hexdigest()

def compary_hash_string(string, hashstring):
    if(hashstring == hash_string(string)):
        return True
    else:
        return False
