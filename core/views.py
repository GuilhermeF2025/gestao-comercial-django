from django.shortcuts import render

def dashboard_view(request):
    # Por enquanto, apenas renderiza a tela. 
    # No futuro, passaremos gráficos e totais de vendas aqui.
    return render(request, 'core/dashboard.html')