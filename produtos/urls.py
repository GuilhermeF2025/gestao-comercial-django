from django.urls import path
from .views import produto_cadastro_view, produto_exportar_view, produto_importar_view, produto_lista_view, produto_deletar_view, produto_editar_view, produto_bulk_deletar_view

app_name = 'produtos'

urlpatterns = [
    # Quando acessar /produtos/cadastro/
    path('cadastro/', produto_cadastro_view, name='cadastro'),
    
    # Quando acessar apenas /produtos/ (A lista será a tela inicial do app)
    path('', produto_lista_view, name='lista'), 
    # Note que usamos <int:pk> para passar o ID do produto na URL
    path('editar/<int:pk>/', produto_editar_view, name='editar'),
    path('deletar/<int:pk>/', produto_deletar_view, name='deletar'),

    path('bulk-deletar/', produto_bulk_deletar_view, name='bulk_deletar'), # <-- NOVA ROTA

    path('exportar/', produto_exportar_view, name='exportar'),
    path('importar/', produto_importar_view, name='importar'),
]