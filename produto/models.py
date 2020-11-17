from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    categoryName = models.CharField(unique=True,max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.categoryName


class Products(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nameproduct = models.CharField(max_length=100, null=False, blank=False)
    descripction = models.TextField(max_length=500, null=False, blank=False)
    price = models.FloatField(max_length=10, null=False)
    discount =  models.FloatField(max_length=10, default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,null=False,blank=False)
    id_user = models.IntegerField(null=False)
    
    def __str__(self):
        return self
