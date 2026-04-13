from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from clientes.models import Customer

@require_POST
def cliente_deletar_view(request, pk):
    cliente = get_object_or_404(Customer, pk=pk)
    cliente.is_active = False # Soft Delete
    cliente.save()
    return HttpResponse("") # HTMX faz a linha sumir

@require_POST
def cliente_bulk_deletar_view(request):
    ids = request.POST.getlist('selected_ids')
    if ids:
        Customer.objects.filter(id__in=ids).update(is_active=False)
    
    clientes = Customer.objects.all()
    return render(request, 'partials/clientes/_tabela.html', {'clientes': clientes})