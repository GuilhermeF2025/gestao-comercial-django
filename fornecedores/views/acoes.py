from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from fornecedores.models import Supplier

@require_POST
def fornecedor_deletar_view(request, pk):
    fornecedor = get_object_or_404(Supplier, pk=pk)
    fornecedor.is_active = False
    fornecedor.save()
    return HttpResponse("")

@require_POST
def fornecedor_bulk_deletar_view(request):
    ids = request.POST.getlist('selected_ids')
    if ids:
        Supplier.objects.filter(id__in=ids).update(is_active=False)
    fornecedores = Supplier.objects.all()
    return render(request, 'partials/fornecedores/_tabela.html', {'fornecedores': fornecedores})