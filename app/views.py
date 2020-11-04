from re import T
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, requires_csrf_token
from .serializers import *
from .models import *
from .email import send_email, validador_email_correct, verificador_email_db
from .users import generetion_token, user_method, verify_login_active, disconect, verify_login_match, verify_fields_none, get_token, verify_token_exists
from .block import verify_ip

def start_view(request):
    # verificando o metodo GET, lembrando que o que defini se o usuario acessa essa funcao esta no arquivo urls.py
    if(request.method == 'GET'):
        # retorno simples em Http
        return JsonResponse(['Welome My Api , :D',{'Usuarios': UsersSerializers(Users.objects.all(), many=True).data}], safe=False)
    else:
        return JsonResponse('Method error brow.', status=400, safe=False)

# csrf_exempt significa que o usuario pode acessar, sem isso o usuario nao tem acesso, padrao do django.


@csrf_exempt
# criando um usuario
def users_create(request):
    if(request.method == 'POST'):
        # verificando se os campos essenciais estao vazios
        if(verify_fields_none(request, 'create')):
            # verificando se existe o email no bd
            if (not verificador_email_db(request.GET.get('email'))):
                # verificando se o email e aceito
                if(validador_email_correct(request)):
                    # enviando o email de ativacao, ainda nao terminado
                    send_email(request,request.GET.get('email'))
                    # criando o usuario
                    return JsonResponse(user_method(request, 'create'), safe=False)

                else:
                    return JsonResponse('Email invalido.', status=400, safe=False)
            else:
                return JsonResponse('Email ja existe', status=400, safe=False)
        else:
            return JsonResponse('Envie: username, email, password', status=400, safe=False)
    return JsonResponse('Metodo errado, tente Post', status=400, safe=False)


@csrf_exempt
def users_login(request):
    if(request.method == 'POST'):
        # metodo ainda nao completo, vai verificar o ip e travar apartir de um certo numero de requisicoes
        verify_ip(request, 5)
        # verificando se os campos estao vazios
        if (verify_fields_none(request, 'login')):
            # verificando se o login e valido
            if(verify_login_match(request)):
                # verificando se o usuario esta logado
                if(verify_login_active(request)):
                    # caso esteja deslogado ele poderá logar
                    return JsonResponse(['Login Sucessfully', {'token': get_token(request)}], safe=False)
                else:
                    return JsonResponse('User logged ', safe=False)
            else:
                return JsonResponse('User or password does not match.', status=400, safe=False)
        else:
            return JsonResponse('Envie: email, password', status=400, safe=False)
    else:
        return JsonResponse('Metodo usado, e diferente do usado para logar.', status=400, safe=False)


@csrf_exempt
def users_logout(request):
    if(request.method == 'POST'):
        # verificando se o campo esta vazio
        if(verify_fields_none(request, 'logout')):
            # verificando se existe o token
            if(verify_token_exists(request)):
                # verificando se o login esta ativo se estiver ja desconecta
                return disconect(request)
            else:
                return JsonResponse('Does not Match', status=400, safe=False)
        else:
            return JsonResponse('Envie: token.', status=400, safe=False)
    else:
        return JsonResponse('Metodo usado, e diferente do usado para logar.', status=400, safe=False)


@csrf_exempt
def users_update(request):
    if(request.method == 'PUT'):
        # verificando se os campos essenciais estao vazios
        if(verify_fields_none(request, 'update')):
            # verificando o token do usuario existe
            if(verify_token_exists(request)):
                # modificando o usuario
                return JsonResponse(user_method(request, 'update'), safe=False)
            else:
                return JsonResponse('Does match exist', status=400, safe=False)
        else:
            return JsonResponse('Campos essenciais vazios', status=400, safe=False)
    
    else:
        return JsonResponse('Metodo de envio errado', status=400, safe=False)


@csrf_exempt
def users_delete(request):
    if(request.method == 'DELETE'):
        # verificando se os campos essenciais estao vazios
        if(verify_fields_none(request, 'delete')):
            # verificando o token do usuario existe
            if(verify_token_exists(request)):
                # deletando o usuario
                return JsonResponse(user_method(request, 'delete'), safe=False)
            else:
                return JsonResponse('Does match exist', status=400, safe=False)
        else:
            return JsonResponse('Campos essenciais vazios', status=400, safe=False)
    return JsonResponse('Metodo de envio errado', status=400, safe=False)


def users_view(request, id_user):
    if(request.method == 'GET'):
        try:
            User = None
            if(Users.objects.get(id=id_user) != None):
                User = Users.objects.filter(id=id_user)
                serializer = UsersSerializers(User, many=True)
                return JsonResponse(serializer.data, safe=False)
        except Users.DoesNotExist:
            return JsonResponse('Usuario nao existe.', status=500, safe=False)


# def users_view_none_params(request):
    if(request.method == 'GET'):
        try:
            User = None

            if(request.GET.get('id') == None):
                User = Users.objects.all()
            else:
                if(Users.objects.get(id=request.GET.get('id'))):
                    if(Users.objects.get(id=request.GET.get('id')) != None):
                        User = Users.objects.filter(id=request.GET.get('id'))

            serializer = UsersSerializers(User, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Users.DoesNotExist:
            return JsonResponse('Usuario nao existe.', status=500, safe=False)


# def products_view_none_params(request):
    if(request.method == 'GET'):
        try:
            Product = None
            if(request.GET.get('id') == None):
                Product = Products.objects.all()
            else:
                if(Products.objects.get(id=request.GET.get('id'))):
                    if(Products.objects.get(id=request.GET.get('id')) != None):
                        Product = Products.objects.filter(
                            id=request.GET.get('id'))

            serializer = ProductsSerializers(Product, many=True)
            return JsonResponse({'products': serializer.data}, safe=False)
        except Products.DoesNotExist:
            return JsonResponse('Produto nao existe.', status=500, safe=False)


def products_view(request, id_product):
    if(request.method == 'GET'):
        try:
            Product = None
            if(Products.objects.get(id=id_product) != None):
                Product = Products.objects.filter(id=id_product)
                serializer = ProductsSerializers(Product, many=True)
                return JsonResponse(serializer.data, safe=False)
        except Products.DoesNotExist:
            return JsonResponse('Produto nao existe.', status=500, safe=False)


@ensure_csrf_cookie
def products_update(request, id_product):
    if(request.method == 'PUT'):
        try:
            product = Products.objects.get(id=id_product)
        except:
            return JsonResponse('Produto nao existe.', status=500, safe=False)
        product.nameproduct = request.GET.get('nameproduct')
        product.descripction = request.GET.get('descripction')
        product.save()
        serializer = ProductsSerializers(product)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse('serializer.errors', status=404)


@ensure_csrf_cookie
def products_delete(request, id_product):
    if(request.method == 'DELETE'):
        try:
            data = None
            Product = Products.objects.get(id=id_product)
        except:
            return JsonResponse('Usuario nao existe.', status=500, safe=False)
        operations = Product.delete()
        data = {}
        if operations:
            data['Seu Produto Foi deletado, '] = ' Com sucesso '
        else:
            data['fail'] = 'Delete failed'
        return JsonResponse(data=data)


@csrf_exempt
def products_create(request):
    if(request.method == 'POST'):
        new_product = Products.objects.create(nameproduct=request.GET.get(
            'nameproduct'), descripction=request.GET.get('descripction'))
        new_product.save()
        serializer = ProductsSerializers(new_product)
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Erro ao Criar', status=400, safe=False)
