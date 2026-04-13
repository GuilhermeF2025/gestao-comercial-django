from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from clientes.models import Customer
from clientes.forms import CustomerForm

def cliente_cadastro_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso_html = """
            <div class="alert alert-success">✅ Cliente cadastrado com sucesso!</div>
            <button class="btn btn-primary mt-3" onclick="location.reload()">Novo Cliente</button>
            """
            return HttpResponse(sucesso_html)
        else:
            return render(request, 'partials/clientes/_form.html', {'form': form})

    form = CustomerForm()
    return render(request, 'clientes/cadastro.html', {'form': form})

def cliente_editar_view(request, pk):
    cliente = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:lista')
    else:
        form = CustomerForm(instance=cliente)
        
    return render(request, 'clientes/cadastro.html', {'form': form, 'cliente': cliente})