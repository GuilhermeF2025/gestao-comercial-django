from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('pdv/', views.pdv_view, name='pdv'),
    path('pdv/<int:pk>/add/', views.pdv_adicionar_item, name='add_item'),
    path('pdv/remove/<int:pk>/', views.pdv_remover_item, name='remove_item'),
    path('pdv/<int:pk>/finalizar/', views.pdv_finalizar_venda, name='finalizar'),
]