from django.shortcuts import render
from clientes.models import Customer

from django.contrib.auth.decorators import login_required, permission_required

@login_required # <-- Adicione esta linha!
@permission_required('clientes.view_customer', raise_exception=True)
def cliente_lista_view(request):
    query = request.GET.get('q', '')

    if query:
        clientes = Customer.objects.filter(name__icontains=query) | Customer.objects.filter(cpf_cnpj__icontains=query)
    else:
        clientes = Customer.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'partials/clientes/_tabela.html', {'clientes': clientes})

    return render(request, 'clientes/lista.html', {'clientes': clientes})