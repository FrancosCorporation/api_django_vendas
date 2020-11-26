from django.urls import path
from . import views

urlpatterns = [
    path('', views.user),
    path('login', views.users_login),
    path('logout', views.users_logout),
    path('change', views.change_level),
    path('activation', views.activation_account),
    path('pki-validation/<str:value>', views.file),
    
]
