from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('account/', include('app.urls')),
   path('.well-known/', include('app.urls')),
   path('', include('produto.urls'))
]
