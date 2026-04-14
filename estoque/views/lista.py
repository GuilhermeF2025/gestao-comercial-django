from django.shortcuts import render
from estoque.models import StockMovement

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