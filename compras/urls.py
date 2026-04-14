from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    # Navegação Principal
    path('', views.compra_lista_view, name='lista'),
    path('nova/', views.compra_criar_view, name='nova'),
    path('<int:pk>/', views.compra_detalhe_view, name='detalhe'),
    
    # Ações HTMX
    path('<int:pk>/add-item/', views.adicionar_item_view, name='adicionar_item'),
    path('remover-item/<int:pk>/', views.remover_item_view, name='remover_item'),
    path('<int:pk>/finalizar/', views.finalizar_compra_view, name='finalizar'),
]