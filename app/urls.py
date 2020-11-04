from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.start_view),
    path('account/create', views.users_create),
    path('account/login', views.users_login),
    path('account/logout', views.users_logout),
    path('account/update', views.users_update),
    path('account/delete', views.users_delete),
]
