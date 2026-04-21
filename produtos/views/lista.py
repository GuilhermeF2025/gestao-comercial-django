from django.shortcuts import render
from produtos.models import Product

from django.contrib.auth.decorators import login_required

@login_required # <-- Adicione esta linha!
def produto_lista_view(request):
    query = request.GET.get('q', '')

    if query:
        produtos = Product.objects.filter(name__icontains=query) | Product.objects.filter(sku__icontains=query)
    else:
        produtos = Product.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'partials/produtos/_tabela.html', {'produtos': produtos})

    return render(request, 'produtos/lista.html', {'produtos': produtos})