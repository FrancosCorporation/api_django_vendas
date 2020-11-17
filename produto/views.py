from produto.others.category import get_all_categorys
from app.others.users import get_level_user, verify_loged
from django.http.response import JsonResponse
from produto.others.fields import verify_fields_none
from app.others.methods import verify_method
from django.views.decorators.csrf import csrf_exempt
from .others.products import get_all_products, products_create, products_delete

# csrf_exempt significa que o usuario pode acessar, sem isso o usuario nao tem acesso, padrao do django.



@csrf_exempt
def return_all_products(request):
    if(verify_method(request, 'GET')):
        if(verify_loged(request)):
            return JsonResponse([{' Todos Produtos ': get_all_products()},{' Todas Categorias ': get_all_categorys()}], safe=False)
        else:
            return JsonResponse({}, status=401)
    else:
        return JsonResponse({}, status=405)


@csrf_exempt
def create_products(request):
    if(verify_method(request, 'POST')):
        if(verify_fields_none(request, 'create')):
                if(verify_loged(request) and (get_level_user(request) >= 2)):
                    if(products_create(request)):
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
def update_produtos(request):
    if(verify_method(request, 'PUT')):
        if(verify_fields_none(request, 'update')):
                if(verify_loged(request) and (get_level_user(request) >= 2)):
                    if(products_create(request)):
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
def delete_produtos(request):
    if(verify_method(request, 'DELETE')):
                if(verify_loged(request) and (get_level_user(request) >= 2)):
                    if(products_delete(request)):
                        return JsonResponse({})
                    else:
                        return JsonResponse({}, status=400)
                else:
                    return JsonResponse({}, status=401)
    else:
        return JsonResponse({}, status=405) 