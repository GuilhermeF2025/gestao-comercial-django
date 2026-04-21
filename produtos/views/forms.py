from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from produtos.forms.product_form import ProductForm
from produtos.models import Product

from django.contrib.auth.decorators import login_required

@login_required # <-- Adicione esta linha!
def produto_cadastro_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso_html = """
            <div class="alert alert-success d-flex align-items-center" role="alert">
                <div>✅ Produto cadastrado com sucesso!</div>
            </div>
            <button class="btn btn-primary mt-3" onclick="location.reload()">Cadastrar Novo</button>
            """
            return HttpResponse(sucesso_html)
        else:
            return render(request, 'partials/produtos/_form.html', {'form': form})

    form = ProductForm()
    return render(request, 'produtos/cadastro.html', {'form': form})


@login_required # <-- Adicione esta linha!
def produto_editar_view(request, pk):
    produto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos:lista')
    else:
        form = ProductForm(instance=produto)
        
    return render(request, 'produtos/cadastro.html', {'form': form, 'produto': produto})