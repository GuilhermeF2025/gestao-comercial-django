from django.urls import path
from . import views

app_name = 'fornecedores'

urlpatterns = [
    path('', views.fornecedor_lista_view, name='lista'),
    path('cadastro/', views.fornecedor_cadastro_view, name='cadastro'),
    path('editar/<int:pk>/', views.fornecedor_editar_view, name='editar'),
    path('deletar/<int:pk>/', views.fornecedor_deletar_view, name='deletar'),
    path('bulk-deletar/', views.fornecedor_bulk_deletar_view, name='bulk_deletar'),
]