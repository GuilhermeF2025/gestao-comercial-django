from django.shortcuts import render
from compras.models import Purchase

from django.contrib.auth.decorators import login_required

@login_required # <-- Adicione esta linha!
def compra_lista_view(request):
    query = request.GET.get('q', '')
    if query:
        compras = Purchase.objects.filter(supplier__name__icontains=query) | \
                  Purchase.objects.filter(invoice_number__icontains=query)
    else:
        compras = Purchase.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'partials/compras/_tabela_compras.html', {'compras': compras})

    return render(request, 'compras/lista.html', {'compras': compras})