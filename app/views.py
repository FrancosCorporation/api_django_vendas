import logging

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .others.block import verify_ip
from .others.email import send_email, validador_email_correct, verificador_email_db
from .others.fields import verify_fields_none
from .others.methods import verify_method
from .others.token import verify_token_exists
from .others.users import (
    actvation_user,
    connecting_user,
    disconect_user,
    get_user_for_email,
    return_user_values,
    user_create,
    user_delete,
    user_update,
    verify_loged,
    verify_login_match,
)


logger = logging.getLogger(__name__)

# These JSON endpoints authenticate protected requests with an explicit Bearer
# header and never use Django's session cookie. CSRF exemption is therefore
# limited to this token-only API; do not add cookie authentication here.
@csrf_exempt
def return_dados_users(request):
    if not verify_method(request, "GET"):
        return JsonResponse({}, status=405)
    if not verify_loged(request):
        return JsonResponse({}, status=401)
    return JsonResponse({"user": return_user_values(request)})


@csrf_exempt
def users_create(request):
    if not verify_method(request, "POST"):
        return JsonResponse({}, status=405)
    if not verify_fields_none(request, "create"):
        return JsonResponse({"error": "Informe username, email e password no corpo."}, status=400)
    if not validador_email_correct(request):
        return JsonResponse({"error": "E-mail inválido."}, status=400)
    if verificador_email_db(request):
        return JsonResponse({"error": "E-mail já cadastrado."}, status=409)
    if not user_create(request):
        return JsonResponse({"error": "Não foi possível criar a conta."}, status=400)

    user = get_user_for_email(request)
    try:
        send_email(user.email, user.username, user.token, request)
    except Exception:
        logger.exception("Não foi possível enviar o e-mail de ativação")
        user.delete()
        return JsonResponse({"error": "Não foi possível enviar o e-mail de ativação."}, status=503)
    return JsonResponse({"message": "Confira seu e-mail para ativar a conta."}, status=201)


@csrf_exempt
def users_login(request):
    if not verify_method(request, "POST"):
        return JsonResponse({}, status=405)
    if not verify_ip(request, 2):
        return JsonResponse({"error": "Muitas tentativas. Aguarde antes de tentar novamente."}, status=429)
    if not verify_fields_none(request, "login"):
        return JsonResponse({"error": "Informe email e password no corpo."}, status=400)
    if not verify_login_match(request):
        return JsonResponse({}, status=401)
    if not connecting_user(request):
        return JsonResponse({"error": "Ative sua conta antes de entrar."}, status=403)

    user = get_user_for_email(request)
    return JsonResponse({"token_type": "Bearer", "access_token": user.token, "expires_in": 3600})


@csrf_exempt
def users_logout(request):
    if not verify_method(request, "POST"):
        return JsonResponse({}, status=405)
    if not verify_fields_none(request, "logout") or not verify_token_exists(request, "normal"):
        return JsonResponse({}, status=401)
    if not disconect_user(request):
        return JsonResponse({}, status=401)
    return JsonResponse({"message": "Sessão encerrada."})


@csrf_exempt
def users_update(request):
    if not verify_method(request, "PUT"):
        return JsonResponse({}, status=405)
    if not verify_fields_none(request, "update") or not verify_loged(request):
        return JsonResponse({"error": "Token inválido ou campos incompletos."}, status=401)
    if not user_update(request):
        return JsonResponse({"error": "Senha atual ou dados de atualização inválidos."}, status=400)
    return JsonResponse({"message": "Conta atualizada. Se a senha mudou, entre novamente."})


@csrf_exempt
def users_delete(request):
    if not verify_method(request, "DELETE"):
        return JsonResponse({}, status=405)
    if not verify_fields_none(request, "delete") or not verify_loged(request):
        return JsonResponse({}, status=401)
    if not user_delete(request):
        return JsonResponse({}, status=401)
    return HttpResponse(status=204)


@csrf_exempt
def activation_account(request):
    if not verify_method(request, "GET"):
        return JsonResponse({}, status=405)
    if not verify_fields_none(request, "active") or not verify_token_exists(request, "active"):
        return JsonResponse({"error": "Link de ativação inválido ou expirado."}, status=400)
    if not actvation_user(request):
        return JsonResponse({"error": "Não foi possível ativar esta conta."}, status=409)
    return JsonResponse({"message": "Conta ativada. Você já pode entrar."})
