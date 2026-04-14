from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from compras.models import Purchase, PurchaseItem
from compras.forms import PurchaseItemForm
from django.db.models import Sum

def recalcular_total_compra(compra):
    total = compra.items.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    compra.total_amount = total
    compra.save(update_fields=['total_amount'])

@require_POST
def adicionar_item_view(request, pk):
    compra = get_object_or_404(Purchase, pk=pk)
    
    # Proteção: Não deixa adicionar itens se a compra já foi finalizada
    if compra.status != 'PENDING':
        return HttpResponse("<div class='alert alert-danger'>Compra já finalizada!</div>")

    form = PurchaseItemForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.purchase = compra
        item.save()
        recalcular_total_compra(compra)
        
        # Devolve a tabela de itens atualizada + formulário limpo
        return render(request, 'partials/compras/_tabela_itens.html', {'compra': compra, 'item_form': PurchaseItemForm()})
    
    # Se der erro de validação, devolve o form com os erros
    return render(request, 'partials/compras/_tabela_itens.html', {'compra': compra, 'item_form': form})

@require_POST
def remover_item_view(request, pk):
    item = get_object_or_404(PurchaseItem, pk=pk)
    compra = item.purchase
    
    if compra.status == 'PENDING':
        item.delete()
        recalcular_total_compra(compra)
        
    return render(request, 'partials/compras/_tabela_itens.html', {'compra': compra, 'item_form': PurchaseItemForm()})