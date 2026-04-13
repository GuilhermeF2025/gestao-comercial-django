from django.contrib import admin
from django.urls import path, include # <-- Importe o include

from core.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    path('produtos/', include('produtos.urls')), # <-- Adicione esta linha
    path('clientes/', include('clientes.urls')), # <-- Adicione esta linha
    path('fornecedores/', include('fornecedores.urls')), # <-- Adicione esta linha
]