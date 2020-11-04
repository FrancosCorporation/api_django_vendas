from django.http.response import JsonResponse
from rest_framework import serializers
from app.serializers import UsersSerializers
from .models import *
from .password import *
from django.utils.timezone import now

 
def user_method(request, method):
    if(method == 'create'):
        user = Users.objects.create(username=username, email=email, password=make_password(password),
                                    last_login=last_login, date_auth=date_auth, token=generetion_token())
        return [{'Created Sucessfully': 'Check your Email For Confirmation'}, {'token': user.token}]

    elif(method == 'delete'):
        user = Users.objects.get(token=token)
        user.delete()
        return ['Delete Sucessfully', {user.username: ' No exist more'}]


def user_update(request):
    email = request.GET.get('email')
    username = request.GET.get('username')
    password = request.GET.get('password')
    last_login = now()
    date_auth = now()
    token = request.GET.get('token')
    elif(method == 'update'):
    try:
        # trazendo o objeto
        user = Users.objects.get(token=token)
        # verificando se o email e igual
        if(user.email == email):
            if(check_password(password, user.password)):
                if(user.username == username):
                    return [{'Update Not Work': 'Not Changed Information'}, user.username]
                else:
                    user.username = username
                    user.last_login = last_login
                    user.save()
                    return [{'Update Sucessfully': 'Check your Email For Confirmation'}, {'Welcome': user.username}]
            else:
                user.password = make_password(password)
                user.username = username
                user.last_login = last_login
                user.save()
                return [{'Update Sucessfully': 'Check your Email For Confirmation'}, {'Welcome': user.username}]
        # nao sendo igual segue por aqui
        else:
            if(not verify_email_existy(request)):
                user.email = email
                user.password = make_password(password)
                user.username = username
                user.last_login = last_login
                user.save()
                return [{'Update Sucessfully': 'Check your Email For Confirmation'}, {'Welcome': user.username}]
            else:
                return ['E-mail already registered']
    except:
        return Exception


def verify_login_match(request):
    email = request.GET.get('email')
    user = Users.objects.get(email=email)
    password = request.GET.get('password')
    if((user.email == email) and (check_password(password, user.password))):
        return True
    else:
        return False


def verify_login_active(request):
    email = request.GET.get('email')
    user = Users.objects.get(email=email)
    if(user.is_active is False):
        user.is_active = True
        user.last_login = now()
        user.save()
        return True
    else:
        return False


def generetion_token():
    return make_password('nome').replace('pbkdf2_sha256$216000$', '').replace('=', '').replace('$', '').replace('+', '').replace('/', '')


def get_token(request):
    user = Users.objects.get(pk=request.GET.get('email'))
    return user.token


def verify_token_exists(request):
    try:
        # vericiando se o token existe
        if(Users.objects.get(token=request.GET.get('token'))):
            return True
        # se nao achar retorna false
    except:
        return False


def disconect(request):
    user = Users.objects.get(token=request.GET.get('token'))
    if(user.is_active == True):
        user.is_active = False
        user.save()
        return JsonResponse("User has been logout  .", safe=False)
    else:
        return JsonResponse("User not conected .", safe=False)


def verify_fields_none(request, method):
    email = request.GET.get('email')
    password = request.GET.get('password')
    username = request.GET.get('username')
    token = request.GET.get('token')
    if((method == 'create')):
        if (((email != None) and (email != '')) and ((password != None) and (password != '')) and ((username != None) and (username != ''))):
            return True
        else:
            return False

    if((method == 'update')):
        if (((email != None) and (email != '')) and ((password != None) and (password != '')) and ((username != None) and (username != '')) and ((token != None) and (token != ''))):
            return True
        else:
            return False

    elif(method == 'login'):
        if(((email != None) and (email != '')) and ((password != None) and (password != ''))):
            return True
        else:
            return False
    elif((method == 'logout') or (method == 'delete')):
        if(((token != None) and (token != ''))):
            return True
        else:
            return False


def verify_email_existy(request):
    email = request.GET.get('email')
    # verificando se o email existe no banco
    try:
        # se o email existir ele retorna True
        if(Users.objects.get(email=email)):
            return True

    # se o email nao existir
    except:
        return False


def return_user_create(request):
    return Users.objects.values(username=request.GET.get('username'), email=request.GET.get('email'), password=make_password(request.GET.get('password')),
                                    last_login=now(), date_auth=now(), token=generetion_token())