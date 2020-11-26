from app.others.fields import verify_fields_none
from app.others.users import get_user_values, verify_loged,user_create, user_update, user_delete
from app.others.email import send_email, verificador_email_db, validador_email_correct
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_get(request):
    # verificando se o campo esta vazio
    if(verify_fields_none(request, 'logout')):
        # verificando se ta logado
        if(verify_loged(request)):
            return JsonResponse([' Dados usuario ', get_user_values(request)], safe=False)
        else:
            return JsonResponse({}, status=401)
    else:
        return JsonResponse({}, status=406)

# criando um usuario
@csrf_exempt
def users_create(request):
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

@csrf_exempt
def users_update(request):
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


@csrf_exempt
def users_delete(request):
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


