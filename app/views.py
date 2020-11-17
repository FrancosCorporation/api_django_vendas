from app.others.block import verify_ip
from app.others.fields import verify_fields_none
from app.others.methods import verify_method
from .others.token import verify_token_exists
from .others.users import actvation_user, change_level, get_all_users, get_token_for_email, get_token_for_email, get_user_for_token, get_level_user, get_user_values, verify_loged, verify_login_match, connecting_user, disconect_user, user_create, user_update, user_delete
from .others.email import send_email, verificador_email_db, validador_email_correct
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# csrf_exempt significa que o usuario pode acessar, sem isso o usuario nao tem acesso, padrao do django.
@csrf_exempt
def return_dados_users(request):
    # verificando o metodo
    if(verify_method(request, 'GET')):
        # verificando se o campo esta vazio
        if(verify_fields_none(request, 'logout')):
            # verificando se ta logado
            if(verify_loged(request)):
                return JsonResponse([' Dados usuario ', get_user_values(request)], safe=False)
            else:
                return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=406)
    else:
        return JsonResponse({}, status=405)

@csrf_exempt
def return_all_users(request):
    if(verify_method(request, 'GET')):
        if(verify_fields_none(request, 'logout')):
            if(verify_loged(request) and (get_level_user(request) >= 2)):
                return JsonResponse([' Todos usuario ', get_all_users()], safe=False)
            else:
                return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=406)
    else:
        return JsonResponse({}, status=405)

# criando um usuario
@csrf_exempt
def users_create(request):
    if(verify_method(request, 'POST')):
        if(verify_fields_none(request, 'create')):
            # verificando se existe o email no bd, ele nao pode existir para passar
            if (not verificador_email_db(request)):
                # verificando se o email e aceito
                if(validador_email_correct(request)):

                    # criando o usuario
                    if(user_create(request)):
                        # enviando o email de ativacao, ainda nao terminado
                        #send_email(request)
                        return JsonResponse({})
                    else:
                        return JsonResponse({}, status=400)

                else:
                    return JsonResponse({}, status=406)
            else:
                return JsonResponse({}, status=409)
        else:
            return JsonResponse({}, status=406)
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
def users_update(request):
    if(verify_method(request, 'PUT')):
        if(verify_fields_none(request, 'update')):
            if(verify_loged(request)):
                # modificando o usuario
                if(user_update(request)):
                    return JsonResponse({})
                else:
                    return JsonResponse({}, status=406)
            else:
                return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=406)

    else:
        return JsonResponse({}, status=405)

@csrf_exempt
def users_delete(request):
    if(verify_method(request, 'DELETE')):
        if(verify_fields_none(request, 'delete')):
            if(verify_loged(request)):
                # deletando o usuario
                if(user_delete(request)):
                    return JsonResponse({})
                else:
                    return JsonResponse({}, status=400)
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


def change_level_user(request):
    if(verify_method(request, 'GET')):
        if(verify_fields_none(request, 'change')):
            if((verify_loged(request)) and (get_level_user(request) == 5)):
                if(change_level(request)):
                    return JsonResponse({'Changed': 'Sucessfull'}, safe=False)
                else:
                    return JsonResponse({}, status=409)

            else:
                return JsonResponse({}, status=401)
        else:
            return JsonResponse({}, status=406)
    else:
        return JsonResponse({}, status=405)
