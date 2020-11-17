from django.urls import path
from . import views

urlpatterns = [
    path('', views.return_all_products),
    path('create', views.create_products),
    path('update', views.update_produtos),
    
]
