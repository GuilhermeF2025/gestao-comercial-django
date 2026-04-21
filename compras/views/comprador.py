from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from compras.models import PurchaseRequest, Purchase, PurchaseItem
from fornecedores.models import Supplier

@login_required
@permission_required('compras.add_purchase', raise_exception=True)
def painel_comprador_view(request):
    """Lista de itens aprovados aguardando cotação/compra"""
    # Só queremos o que está APPROVED. Se já estiver COMPLETED, já foi comprado.
    aprovados = PurchaseRequest.objects.filter(status='APPROVED').order_by('created_at')
    return render(request, 'compras/comprador_painel.html', {'aprovados': aprovados})

@login_required
@permission_required('compras.add_purchase', raise_exception=True)
def iniciar_compra_da_solicitacao(request, req_pk):
    """
    Transforma uma solicitação num Pedido de Compra.
    O Comprador escolhe o fornecedor e o sistema pré-preenche os dados.
    """
    requisicao = get_object_or_404(PurchaseRequest, pk=req_pk, status='APPROVED')
    
    if request.method == 'POST':
        fornecedor_id = request.POST.get('supplier')
        fornecedor = get_object_or_404(Supplier, pk=fornecedor_id)
        
        # 1. Cria a 'Capa' do Pedido de Compra
        novo_pedido = Purchase.objects.create(
            supplier=fornecedor,
            issue_date=requisicao.created_at.date(), # Ou data atual
            status='PENDING',
            created_by=request.user
        )
        
        # 2. Cria o Item do Pedido vinculado à solicitação original
        PurchaseItem.objects.create(
            purchase=novo_pedido,
            product=requisicao.product,
            origin_request=requisicao,
            quantity=requisicao.quantity,
            unit_cost=requisicao.product.average_cost, # Sugere o custo atual
            total_cost=requisicao.quantity * requisicao.product.average_cost
        )
        
        # 3. Atualiza o estado da solicitação (Agora está em processo de compra)
        requisicao.status = 'COMPLETED'
        requisicao.save()
        
        return redirect('compras:detalhe', pk=novo_pedido.pk)

    fornecedores = Supplier.objects.all()
    return render(request, 'compras/converter_solicitacao.html', {
        'requisicao': requisicao,
        'fornecedores': fornecedores
    })