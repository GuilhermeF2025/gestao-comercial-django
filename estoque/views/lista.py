from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from estoque.models import StockMovement

# --- REGRA DE AUTORIZAÇÃO ---
# Esta função verifica se o usuário tem o poder de "Chefe" (Admin)
def is_admin(user):
    return user.is_superuser

# --- A CEBOLA DE SEGURANÇA ---
@login_required # 1º: Tem que estar logado
@user_passes_test(is_admin, login_url='/pdv/') # 2º: Tem que ser Chefe (se não, volta pro caixa)
def movimentacao_lista_view(request):
    query = request.GET.get('q', '')
    
    if query:
        movimentacoes = StockMovement.objects.filter(product__name__icontains=query) | \
                        StockMovement.objects.filter(reason__icontains=query)
    else:
        # Traz as 100 últimas movimentações para não sobrecarregar a tela
        movimentacoes = StockMovement.objects.all()[:100]

    if request.headers.get('HX-Request'):
        return render(request, 'partials/estoque/_tabela.html', {'movimentacoes': movimentacoes})

    return render(request, 'estoque/lista.html', {'movimentacoes': movimentacoes})