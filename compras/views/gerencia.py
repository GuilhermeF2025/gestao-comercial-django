from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from compras.models import PurchaseRequest

@login_required
@permission_required('compras.change_purchaserequest', raise_exception=True)
def requisicoes_pendentes_view(request):
    """Lista apenas o que precisa de atenção da Gerência"""
    requisicoes = PurchaseRequest.objects.filter(status='PENDING').order_by('created_at')
    
    # Se for HTMX, devolvemos apenas a tabela (útil após uma ação)
    if request.headers.get('HX-Request'):
        return render(request, 'partials/compras/_tabela_pendentes.html', {'requisicoes': requisicoes})
        
    return render(request, 'compras/requisicoes_pendentes.html', {'requisicoes': requisicoes})

@login_required
@require_POST
@permission_required('compras.change_purchaserequest', raise_exception=True)
def avaliar_requisicao_view(request, pk):
    """Ação de Aprovar ou Rejeitar"""
    requisicao = get_object_or_404(PurchaseRequest, pk=pk)
    acao = request.POST.get('acao') # 'approve' ou 'reject'
    
    if requisicao.status == 'PENDING':
        if acao == 'approve':
            requisicao.status = 'APPROVED'
        elif acao == 'reject':
            requisicao.status = 'REJECTED'
            
        requisicao.evaluated_by = request.user
        requisicao.save()

    # Retornamos a lista atualizada de pendências via HTMX
    requisicoes = PurchaseRequest.objects.filter(status='PENDING').order_by('created_at')
    return render(request, 'partials/compras/_tabela_pendentes.html', {'requisicoes': requisicoes})