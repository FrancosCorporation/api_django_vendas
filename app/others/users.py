from app.others.block import add_ip_blacklist
from app.serializers import UsersSerializers
from app.others.token import generetion_token
from ..models import *
from .password import *
from django.utils.timezone import now


def user_create(request):
    try:
        data = {'username': request.GET.get('username'), 'email': request.GET.get('email'), 'password': make_password(request.GET.get('password')),
                'last_login': now(), 'date_auth': now(), 'token': generetion_token()}
        serializede = UsersSerializers(data=data)
        if(serializede.is_valid()):
            serializede.save()
            return True
        else:
            return False
    except:
        return False


def user_delete(request):
    try:
        user = Users.objects.get(token=request.GET.get('token'))
        user.delete()
        return True
    except:
        return False


def user_update(request):
    email = request.GET.get('email')
    username = request.GET.get('username')
    password = request.GET.get('password')
    token = request.GET.get('token')
    user = Users.objects.get(token=token)
    # trazendo o objeto
    # verificando se o email e igual
    if(user.email == email and check_password(password, user.password) and user.username == username):
        return False

    elif(user.email == email and check_password(password, user.password)):
        user.username = username
        data = {'username': user.username, 'email': user.email, 'password': user.password, 'last_login': user.last_login,
                'date_auth': user.date_auth, 'token': user.token}
        serializers = UsersSerializers(user, data=data)
        if(serializers.is_valid()):
            serializers.save()
            return True
        else:
            return False

    elif(user.email == email and check_password(password, user.password) == False):
        user.email = email
        user.username = username
        data = {'username': user.username, 'email': user.email, 'password': make_password(password), 'last_login': user.last_login,
                'date_auth': user.date_auth, 'token': user.token}
        serializers = UsersSerializers(user, data=data)
        if(serializers.is_valid()):
            serializers.save()
            return True
        else:
            return False


def verify_login_match(request):
    email = request.GET.get('email')
    user = Users.objects.get(email=email)
    password = request.GET.get('password')
    if((user.email == email) and (check_password(password, user.password))):
        return True
    else:
        add_ip_blacklist(request)
        return False


def connecting_user(request):
    email = request.GET.get('email')
    user = Users.objects.get(email=email)
    if(user.is_active is False and user.activate == True):
        user.is_active = True
        user.last_login = now()
        user.save()
        return True
    else:
        return False


def get_user_for_token(request):
    return Users.objects.get(token=request.GET.get('token'))


def get_user_for_email(request):
    try:
        if(Users.objects.get(email=request.GET.get('email'))):
            return Users.objects.get(email=request.GET.get('email'))
    except:
        return None


def disconect_user(request):
    user = Users.objects.get(token=request.GET.get('token'))
    if(user.is_active == True and user.activate == True):
        user.is_active = False
        user.save()
        return True
    else:
        return False


def return_user_values(request):
    user = Users.objects.get(token=request.GET.get('token'))
    return {'username': user.username, 'email': user.email, 'token': user.token, 'date_last_login': user.last_login}


def actvation_user(request):
    new_list = request.META['QUERY_STRING'].split('=')
    token = new_list[1].replace('/', '')
    user = Users.objects.get(token=token)
    if user.activate is False:
        data = {'username': user.username, 'email': user.email, 'password': user.password, 'last_login': user.last_login,
                'date_auth': user.date_auth, 'token': user.token, 'activate': True}
        serializers = UsersSerializers(user, data=data)
        if(serializers.is_valid()):
            serializers.save()
            return True
        else:
            return False

    else:
        return False


def verify_loged(request):
    user = Users.objects.get(token=request.GET.get('token'))
    duration = 1  # minutos
    new_time = now() - user.last_login
    print((duration/60), (new_time.seconds/3600))
    if((user.activate == True) and (user.is_active == True) and ((new_time.seconds/3600) <= (duration/60))):
        return True
    else:
        data = {'username': user.username, 'email': user.email, 'password': user.password, 'last_login': user.last_login,
                'date_auth': user.date_auth, 'token': user.token, 'is_active': False}
        serializers = UsersSerializers(user, data=data)
        if(serializers.is_valid()):
            serializers.save()
        return False
