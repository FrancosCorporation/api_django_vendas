from django.db import models
# crie seus modelos de tabelas.


class Products(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nameproduct = models.CharField(max_length=100, null=False, blank=False)
    descripction = models.TextField(max_length=500, null=False, blank=False)
    
    
    def __str__(self):
        return self



class Users(models.Model):
    email = models.EmailField(primary_key=True, max_length=100, null=False)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    last_login = models.DateTimeField(null=False)
    date_auth = models.DateTimeField(null=False)
    token = models.TextField(unique=True ,max_length=164, null=False)
    is_active = models.BooleanField(auto_created=True, default=False)
    activate =  models.BooleanField(auto_created=True, default=False)
    
    
    def __str__(self):
        return self
        


class Ip(models.Model):
    ip_address = models.GenericIPAddressField(primary_key=True)
    count = models.IntegerField()
    date_last_try = models.DateTimeField()

    def __str__(self):
        return self
