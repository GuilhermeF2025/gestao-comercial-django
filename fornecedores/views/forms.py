from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from fornecedores.models import Supplier
from fornecedores.forms import SupplierForm

def fornecedor_cadastro_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("""
            <div class="alert alert-success">✅ Fornecedor cadastrado!</div>
            <button class="btn btn-primary mt-3" onclick="location.reload()">Novo Fornecedor</button>
            """)
        return render(request, 'partials/fornecedores/_form.html', {'form': form})

    form = SupplierForm()
    return render(request, 'fornecedores/cadastro.html', {'form': form})

def fornecedor_editar_view(request, pk):
    fornecedor = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('fornecedores:lista')
    else:
        form = SupplierForm(instance=fornecedor)
    return render(request, 'fornecedores/cadastro.html', {'form': form, 'fornecedor': fornecedor})