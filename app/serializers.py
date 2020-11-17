from rest_framework import serializers
from .models import Classificacao, Users,Ip


class ClassificacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Classificacao
        fields = '__all__'


class IpSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ip
        fields = '__all__'

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
