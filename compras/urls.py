from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    # --- SOLICITAÇÕES DE COMPRA (Estoquista / Gerência) ---
    path('solicitacoes/', views.requisicao_lista_view, name='requisicao_lista'),
    path('solicitacoes/nova/', views.requisicao_criar_view, name='requisicao_nova'),
    
    # Navegação Principal
    path('', views.compra_lista_view, name='lista'),
    path('nova/', views.compra_criar_view, name='nova'),
    path('<int:pk>/', views.compra_detalhe_view, name='detalhe'),
    
    # Ações HTMX
    path('<int:pk>/add-item/', views.adicionar_item_view, name='adicionar_item'),
    path('remover-item/<int:pk>/', views.remover_item_view, name='remover_item'),
    path('<int:pk>/finalizar/', views.finalizar_compra_view, name='finalizar'),

    # --- VISÃO DA GERÊNCIA ---
    path('aprovações/', views.requisicoes_pendentes_view, name='requisicoes_pendentes'),
    path('aprovações/<int:pk>/avaliar/', views.avaliar_requisicao_view, name='avaliar_requisicao'),

    # ...
    path('painel-compras/', views.painel_comprador_view, name='painel_comprador'),
    path('solicitacao/<int:req_pk>/comprar/', views.iniciar_compra_da_solicitacao, name='converter_solicitacao'),
]