from django.shortcuts import render, get_object_or_404, redirect
from compras.models import Purchase
from compras.forms import PurchaseForm, PurchaseItemForm

def compra_criar_view(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            if request.user.is_authenticated:
                compra.created_by = request.user
            compra.save()
            # Ao criar a capa, redireciona para a "Área de Trabalho" deste pedido
            return redirect('compras:detalhe', pk=compra.pk)
    else:
        form = PurchaseForm()
    return render(request, 'compras/cadastro.html', {'form': form})

def compra_detalhe_view(request, pk):
    """Área de Trabalho do Pedido (Onde adicionamos os itens)"""
    compra = get_object_or_404(Purchase, pk=pk)
    item_form = PurchaseItemForm()
    
    return render(request, 'compras/detalhe.html', {
        'compra': compra,
        'item_form': item_form
    })