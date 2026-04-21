from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import ProtectedError

from produtos.models import Category
from produtos.forms import CategoryForm

from django.contrib.auth.decorators import login_required

@login_required # <-- Adicione esta linha!
def categoria_lista_view(request):
    query = request.GET.get('q', '')
    if query:
        categorias = Category.objects.filter(name__icontains=query)
    else:
        categorias = Category.objects.all()

    if request.headers.get('HX-Request'):
        return render(request, 'partials/produtos/_tabela_categorias.html', {'categorias': categorias})

    return render(request, 'produtos/categorias/lista.html', {'categorias': categorias})


@login_required # <-- Adicione esta linha!
def categoria_cadastro_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso_html = """
            <div class="alert alert-success">✅ Categoria cadastrada!</div>
            <button class="btn btn-primary mt-3" onclick="location.reload()">Nova Categoria</button>
            """
            return HttpResponse(sucesso_html)
        return render(request, 'partials/produtos/_form_categoria.html', {'form': form})

    form = CategoryForm()
    return render(request, 'produtos/categorias/cadastro.html', {'form': form})


@login_required # <-- Adicione esta linha!
def categoria_editar_view(request, pk):
    categoria = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('produtos:categoria_lista')
    else:
        form = CategoryForm(instance=categoria)
        
    return render(request, 'produtos/categorias/cadastro.html', {'form': form, 'categoria': categoria})


@login_required # <-- Adicione esta linha!
@require_POST
def categoria_deletar_view(request, pk):
    categoria = get_object_or_404(Category, pk=pk)
    try:
        categoria.delete()
        return HttpResponse("") # Some da tela com HTMX
    except ProtectedError:
        # Se houver produtos usando esta categoria, devolvemos um script de alerta nativo
        return HttpResponse("<script>alert('Acesso Negado: Existem produtos vinculados a esta categoria.');</script>")