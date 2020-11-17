from django.db import models
# crie seus modelos de tabelas.


class Classificacao(models.Model):
    id = models.AutoField(primary_key=True)
    create = models.BooleanField(auto_created=True,default=False)
    update = models.BooleanField(auto_created=True,default=False)
    delete = models.BooleanField(auto_created=True,default=False)

    def __str__(self):
        return self.id

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=100, null=False)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    last_login = models.DateTimeField(null=False)
    date_auth = models.DateTimeField(null=False)
    token = models.TextField(unique=True, max_length=164, null=False)
    is_active = models.BooleanField(auto_created=True, default=False)
    activate = models.BooleanField(auto_created=True, default=False)
    permission = models.ForeignKey(
        Classificacao, on_delete=models.CASCADE, default=lambda : Classificacao.objects.create().id)
    group = models.CharField(max_length=15, default='padrao')
    session = models.CharField(max_length=100, default='')

    def __str__(self):
        return self
        

class Ip(models.Model):
    ip_address = models.GenericIPAddressField(primary_key=True)
    count = models.IntegerField()
    date_last_try = models.DateTimeField()

    def __str__(self):
        return self