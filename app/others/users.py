from app.others.block import add_ip_blacklist
from app.serializers import UsersSerializers
from app.others.token import compary_hash_string, generetion_token, hash_string
from ..models import *
from django.utils.timezone import now


def user_create(request):
    try:
        data = {'username': request.GET.get('username'), 'email': request.GET.get('email'), 'password': hash_string(request.GET.get('password')),
                'last_login': now(), 'date_auth': now(), 'token': generetion_token(), 'permission':Classificacao.objects.create().id}
        serializede = UsersSerializers(data=data)
        if(serializede.is_valid()):
            serializede.save()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def user_delete(request):
    try:
        user = Users.objects.get(token=request.GET.get('token'))
        Classificacao.objects.filter(id=user.permission_id).delete()
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
    if(user.email == email and compary_hash_string(password, user.password) and user.username == username):
        return False

    elif(user.email == email and compary_hash_string(password, user.password)):
        user.username = username
        data = {'username': user.username, 'email': user.email, 'password': user.password, 'last_login': user.last_login,
                'date_auth': user.date_auth, 'token': user.token}
        serializers = UsersSerializers(user, data=data)
        if(serializers.is_valid()):
            serializers.save()
            return True
        else:
            return False

    elif(user.email == email and compary_hash_string(password, user.password) == False):
        user.email = email
        user.username = username
        data = {'username': user.username, 'email': user.email, 'password': hash_string(password), 'last_login': user.last_login,
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
    if((user.email == email) and (compary_hash_string(password, user.password))):
        return True
    else:
        add_ip_blacklist(request)
        return False

def connecting_user(request):
    email = request.GET.get('email')
    user = Users.objects.get(email=email)
    if(user.activate == True):
        user.token = generetion_token()
        user.is_active = True
        user.last_login = now()
        user.save()
        return True
    else:
        return False

def get_user_for_token(request):
    return Users.objects.get(token=request.GET.get('token'))

def get_token_for_email(request):
    try:
        if(Users.objects.get(email=request.GET.get('email'))):
            return Users.objects.get(email=request.GET.get('email')).token
    except:
        return None

def get_all_users():
    return UsersSerializers(Users.objects.all(), many=True).data

def disconect_user(request):
    user = get_user_for_token(request)
    if(user.is_active == True and user.activate == True):
        user.is_active = False
        user.save()
        return True
    else:
        return False

def get_user_values(request):
    user = get_user_for_token(request)
    return {'username': user.username, 'email': user.email, 'token': user.token, 'date_last_login': user.last_login}

def actvation_user(request):
    new_list = request.META['QUERY_STRING'].split('=')
    token = new_list[1].replace('/', '')
    user = get_user_for_token(token)
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
    try:
        user = get_user_for_token(request)
        duration = 480  # minutos
        new_time = now() - user.last_login
        # faz a comparacao olhando a cada request de verificacao de usuario
        #print((duration/60), (new_time.seconds/3600))
        if((user.activate == True) and (user.is_active == True) and ((new_time.seconds/3600) <= (duration/60))):
            return True
        else:
            data = {'username': user.username, 'email': user.email, 'password': user.password, 'last_login': user.last_login,
                    'date_auth': user.date_auth, 'token': user.token, 'is_active': False}
            serializers = UsersSerializers(user, data=data)
            if(serializers.is_valid()):
                serializers.save()
                return False
    except:
        return False

def get_permission_su(request):
    try:
        return Classificacao.objects.get(id=Users.objects.get(token=request.GET.get('token')).permission_id).superuser
    except:
        return False

def change_level_user(request):
    try:
        create= False
        update = False
        delete = False
        superuser= False
        if(request.GET.get('create')=='True'):
            create = True
        elif(request.GET.get('update')=='True'):
            update = True
        elif(request.GET.get('delete')=='True'):
            delete =True
        elif(request.GET.get('superuser')=='True'):
            superuser=True
        classsificacao_user = Classificacao.objects.get(id=Users.objects.get(email=request.GET.get('email')).permission_id)
        classsificacao_user.create=create
        classsificacao_user.update=update
        classsificacao_user.delete=delete
        classsificacao_user.superuser=superuser
        classsificacao_user.save()
        return True
    except:
        return False

def get_permission_create(request):
    try:
        classificacao = Classificacao.objects.get(id=Users.objects.get(token=request.GET.get('token')).permission_id)
        if(classificacao.create or classificacao.superuser):
            return True
        else:
            return False
    except:
        return False