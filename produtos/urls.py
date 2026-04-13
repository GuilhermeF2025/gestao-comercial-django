from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # --- PRODUTOS ---
    path('', views.produto_lista_view, name='lista'),
    path('cadastro/', views.produto_cadastro_view, name='cadastro'),
    path('editar/<int:pk>/', views.produto_editar_view, name='editar'),
    path('deletar/<int:pk>/', views.produto_deletar_view, name='deletar'),
    path('bulk-deletar/', views.produto_bulk_deletar_view, name='bulk_deletar'),
    path('exportar/', views.produto_exportar_view, name='exportar'),
    path('importar/', views.produto_importar_view, name='importar'),

    # --- CATEGORIAS ---
    path('categorias/', views.categoria_lista_view, name='categoria_lista'),
    path('categorias/cadastro/', views.categoria_cadastro_view, name='categoria_cadastro'),
    path('categorias/editar/<int:pk>/', views.categoria_editar_view, name='categoria_editar'),
    path('categorias/deletar/<int:pk>/', views.categoria_deletar_view, name='categoria_deletar'),
]