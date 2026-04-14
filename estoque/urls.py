from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.movimentacao_lista_view, name='lista'),
    path('ajuste/', views.ajuste_cadastro_view, name='ajuste'),
]