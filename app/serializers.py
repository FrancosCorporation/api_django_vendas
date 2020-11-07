from rest_framework import serializers
from .models import Users, Products, Ip


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class IpSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ip
        fields = '__all__'

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        #quantidade de itens carregados juntos depth=1
