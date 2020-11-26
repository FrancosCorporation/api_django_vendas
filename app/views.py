from app.others.functions_users import user_get, users_create, users_delete, users_update
import os
from django.http.response import HttpResponse
from app.others.block import verify_ip
from app.others.fields import verify_fields_none
from app.others.methods import verify_method
from .others.token import verify_token_exists
from .others.users import actvation_user, change_level_user,get_permission_su, get_token_for_email, get_token_for_email, verify_loged, verify_login_match, connecting_user, disconect_user
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# csrf_exempt significa que o usuario pode acessar, sem isso o usuario nao tem acesso, padrao do django.
@csrf_exempt
def user(request):
    # verificando o metodo
    if(verify_method(request, 'GET')):
        return user_get(request)
    elif(verify_method(request, 'POST')):
        return users_create(request)
    elif(verify_method(request, 'PUT')):
        return users_update(request)
    elif(verify_method(request, 'DELETE')):
        return users_delete(request)
    else:
        return JsonResponse({}, status=405)

@csrf_exempt
def users_login(request):
    if(verify_method(request, 'POST')):
        # metodo ainda nao completo, vai verificar o ip e travar apartir de um certo numero de requisicoes
        if(verify_ip(request, 2)):
            # verificando se os campos estao vazios
            if (verify_fields_none(request, 'login')):
                # verificando se o login e valido
                if(verify_login_match(request)):
                    # verificando se o usuario esta logado
                    if(connecting_user(request)):
                        # caso esteja deslogado ele poderá logar
                        return JsonResponse({'token': get_token_for_email(request)}, safe=False)
                    else:
                        return JsonResponse({}, status=409)
                else:
                    return JsonResponse({}, status=401)
            else:
                return JsonResponse({}, status=406)
        else:
            return JsonResponse({}, status=423)

    else:
        return JsonResponse({}, status=405)

@csrf_exempt
def users_logout(request):
    if(verify_method(request, 'POST')):
        # verificando se o campo esta vazio
        if(verify_fields_none(request, 'logout')):
            # verificando se existe o token
            if(verify_token_exists(request, 'normal')):
                # verificando se o login esta ativo se estiver ja desconecta
                if(disconect_user(request)):
                    return JsonResponse({}, safe=False)
                else:
                    return JsonResponse({}, status=409)
            else:
                return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=406)
    else:
        return JsonResponse({}, status=405)

@csrf_exempt
def activation_account(request):
    if(verify_method(request, 'GET')):
        if(verify_fields_none(request, 'activation')):
            if(verify_token_exists(request, 'active')):
                if(actvation_user(request)):
                    return JsonResponse({})
                else:
                    return JsonResponse({}, status=409)
            else:
                return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=406)
    else:
        return JsonResponse({}, status=405)

@csrf_exempt
def change_level(request):
    if(verify_method(request, 'PUT')):
        if(verify_fields_none(request, 'change')):
            if((verify_loged(request)) and get_permission_su(request)):
                if(change_level_user(request)):
                    return JsonResponse({})
                else:
                    return JsonResponse({}, status=401)
            else:
                return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=406)
    else:
        return JsonResponse({}, status=405)


def file(request, value):
    print(value)
    caminho = os.path.abspath('app/'+value)
    file = open(caminho, 'r', encoding='utf-8')
    return HttpResponse(file.read())
