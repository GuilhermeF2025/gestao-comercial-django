from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView # <-- Adicione o TemplateView aqui

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redireciona a raiz para o PDV (ou para o dashboard, como preferir)
    path('', RedirectView.as_view(pattern_name='vendas:pdv', permanent=False)),
    
    # Reconectando o seu Dashboard do passado!
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    
    # Rotas de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Nossos Apps
    path('produtos/', include('produtos.urls')),
    path('clientes/', include('clientes.urls')),
    path('fornecedores/', include('fornecedores.urls')),
    path('estoque/', include('estoque.urls')),
    path('compras/', include('compras.urls')),
    path('', include('vendas.urls')),
]