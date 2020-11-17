from app.models import Users
from produto.serializers import ProductsSerializers
from produto.models import Category, Products


def products_create(request):
    try:
        data = {'nameproduct':request.GET.get('nameproduct'), 'descripction':request.GET.get('descripction'),'price':float(request.GET.get('price').replace(',','.')),
        'category':Category.objects.values('categoryName').filter(request.GET.get('category')), 'id_user': Users.objects.get(token=request.GET.get('token')).id}
        if(request.GET.get('discount')!=None):
            data['discount'] = float(request.GET.get('discount').replace(',','.'))
        serializede = ProductsSerializers(data=data)
        if(serializede.is_valid()):
            serializede.save()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False



def products_delete(request):
    try:
        product = Products.objects.get(id=request.GET.get('id'))
        product.delete()
        return True
    except:
        return False



def get_all_products():
    return ProductsSerializers(Products.objects.all(), many=True).data

