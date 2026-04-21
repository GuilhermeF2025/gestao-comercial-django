from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from fornecedores.models import Supplier

from django.contrib.auth.decorators import login_required, permission_required

@login_required # <-- Adicione esta linha!
@permission_required('clientes.add_customer', raise_exception=True)
@require_POST
def fornecedor_deletar_view(request, pk):
    fornecedor = get_object_or_404(Supplier, pk=pk)
    fornecedor.is_active = False
    fornecedor.save()
    return HttpResponse("")


@login_required # <-- Adicione esta linha!
@require_POST
@permission_required('clientes.add_customer', raise_exception=True)
def fornecedor_bulk_deletar_view(request):
    ids = request.POST.getlist('selected_ids')
    if ids:
        Supplier.objects.filter(id__in=ids).update(is_active=False)
    fornecedores = Supplier.objects.all()
    return render(request, 'partials/fornecedores/_tabela.html', {'fornecedores': fornecedores})