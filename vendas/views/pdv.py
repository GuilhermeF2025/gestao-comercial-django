from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from vendas.models import Sale, SaleItem
from vendas.forms import PDVItemForm, PDVCheckoutForm
from django.db.models import Sum

def recalcular_total_venda(venda):
    total = venda.items.aggregate(Sum('total_price'))['total_price__sum'] or 0
    venda.total_amount = total
    venda.save(update_fields=['total_amount'])

def pdv_view(request):
    """Abre o Caixa. Se o usuário já tiver uma venda aberta, recupera ela. Se não, cria uma nova."""
    if request.user.is_authenticated:
        venda, created = Sale.objects.get_or_create(
            status='PENDING', 
            created_by=request.user,
            defaults={'total_amount': 0}
        )
    else:
        return HttpResponse("Você precisa estar logado para acessar o PDV.")

    item_form = PDVItemForm()
    checkout_form = PDVCheckoutForm(instance=venda)

    return render(request, 'vendas/pdv.html', {
        'venda': venda,
        'item_form': item_form,
        'checkout_form': checkout_form
    })

def pdv_adicionar_item(request, pk):
    venda = get_object_or_404(Sale, pk=pk, status='PENDING')
    form = PDVItemForm(request.POST)
    
    erro = None
    if form.is_valid():
        produto = form.cleaned_data['product']
        quantidade = form.cleaned_data['quantity']

        # TRAVA DE SEGURANÇA: Bloqueia venda se não tiver estoque!
        if produto.current_stock < quantidade:
            erro = f"Estoque insuficiente! Você só tem {produto.current_stock} unidades de {produto.name}."
        else:
            item = form.save(commit=False)
            item.sale = venda
            item.save() # O método save do model já vai fotografar o preço e o custo!
            recalcular_total_venda(venda)
            form = PDVItemForm() # Limpa o form para o próximo produto

    return render(request, 'partials/vendas/_carrinho.html', {
        'venda': venda, 
        'item_form': form,
        'erro': erro
    })

def pdv_remover_item(request, pk):
    item = get_object_or_404(SaleItem, pk=pk)
    venda = item.sale
    
    if venda.status == 'PENDING':
        item.delete()
        recalcular_total_venda(venda)
        
    return render(request, 'partials/vendas/_carrinho.html', {
        'venda': venda, 
        'item_form': PDVItemForm()
    })

def pdv_finalizar_venda(request, pk):
    venda = get_object_or_404(Sale, pk=pk, status='PENDING')
    
    if venda.items.count() == 0:
        return HttpResponse("<script>alert('Adicione pelo menos um produto!');</script>")

    form = PDVCheckoutForm(request.POST, instance=venda)
    if form.is_valid():
        venda = form.save(commit=False)
        venda.status = 'COMPLETED'
        venda.save() # <-- AQUI A MÁGICA ACONTECE! Dispara o Signal FIFO e desconta o estoque.
        
        # Redireciona dando um "refresh" na página, o que abrirá um novo caixa vazio automaticamente
        return HttpResponse("<script>location.reload();</script>")
        
    return HttpResponse("<script>alert('Erro ao finalizar. Verifique a forma de pagamento.');</script>")