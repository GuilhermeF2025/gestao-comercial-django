from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from compras.models import Purchase

from django.contrib.auth.decorators import login_required

@login_required # <-- Adicione esta linha!
@require_POST
def finalizar_compra_view(request, pk):
    compra = get_object_or_404(Purchase, pk=pk)
    
    if compra.items.count() == 0:
        return HttpResponse("<script>alert('Erro: A nota fiscal precisa ter pelo menos um item!');</script>")

    if compra.status == 'PENDING':
        compra.status = 'COMPLETED'
        compra.save() # <-- ISSO DISPARA O SIGNAL DO FIFO E ESTOQUE!
        
        # Como o HTMX chamou, retornamos um script para recarregar a página e mostrar tudo bloqueado
        return HttpResponse("<script>location.reload();</script>")
        
    return HttpResponse("")