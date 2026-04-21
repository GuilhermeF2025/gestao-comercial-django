from django.shortcuts import render
from fornecedores.models import Supplier

from django.contrib.auth.decorators import login_required, permission_required

@login_required # <-- Adicione esta linha!
@permission_required('clientes.add_customer', raise_exception=True)
def fornecedor_lista_view(request):
    query = request.GET.get('q', '')
    if query:
        fornecedores = Supplier.objects.filter(name__icontains=query) | Supplier.objects.filter(cnpj__icontains=query)
    else:
        fornecedores = Supplier.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'partials/fornecedores/_tabela.html', {'fornecedores': fornecedores})

    return render(request, 'fornecedores/lista.html', {'fornecedores': fornecedores})