from django.db.models import query
from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import *


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


