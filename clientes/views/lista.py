from django.shortcuts import render
from clientes.models import Customer

def cliente_lista_view(request):
    query = request.GET.get('q', '')

    if query:
        clientes = Customer.objects.filter(name__icontains=query) | Customer.objects.filter(cpf_cnpj__icontains=query)
    else:
        clientes = Customer.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'partials/clientes/_tabela.html', {'clientes': clientes})

    return render(request, 'clientes/lista.html', {'clientes': clientes})