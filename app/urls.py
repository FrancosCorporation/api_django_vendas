from django.urls import path
from . import views

urlpatterns = [
    path('users', views.return_dados_users),
    path('create', views.users_create),
    path('login', views.users_login),
    path('logout', views.users_logout),
    path('update', views.users_update),
    path('delete', views.users_delete),
    path('activation/', views.activation_account)
    
]
