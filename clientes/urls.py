from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_lista_view, name='lista'),
    path('cadastro/', views.cliente_cadastro_view, name='cadastro'),
    path('editar/<int:pk>/', views.cliente_editar_view, name='editar'),
    path('deletar/<int:pk>/', views.cliente_deletar_view, name='deletar'),
    path('bulk-deletar/', views.cliente_bulk_deletar_view, name='bulk_deletar'),
]