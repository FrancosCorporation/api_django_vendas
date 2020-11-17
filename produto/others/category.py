from produto.serializers import CategorySerializers
from produto.models import Category

def get_all_categorys():
    return CategorySerializers(Category.objects.all(), many=True).data