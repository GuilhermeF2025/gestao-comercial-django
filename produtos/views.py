from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm
from .models import Product

from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

import csv
from django.http import HttpResponse
from .resources import ProductResource
from tablib import Dataset

def produto_cadastro_view(request):
    # 1. Se o usuário clicou no botão "Salvar" (POST via HTMX)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        
        if form.is_valid():
            form.save() # Salva no banco de dados!
            
            # Como foi o HTMX que pediu, não recarregamos a página.
            # Devolvemos apenas um fragmento HTML verde de sucesso.
            sucesso_html = """
            <div class="alert alert-success d-flex align-items-center" role="alert">
                <div>✅ Produto cadastrado com sucesso!</div>
            </div>
            <button class="btn btn-primary mt-3" onclick="location.reload()">Cadastrar Novo</button>
            """
            return HttpResponse(sucesso_html)
        
        else:
            # Se deu erro (ex: faltou o SKU), devolvemos APENAS o formulário atualizado 
            # com as mensagens de erro em vermelho, sem recarregar a tela.
            return render(request, 'partials/produtos/_form.html', {'form': form})

    # 2. Se o usuário apenas acessou a página pelo menu (GET)
    form = ProductForm()
    return render(request, 'produtos/cadastro.html', {'form': form})


def produto_lista_view(request):
    # 1. Capturamos o que o usuário digitou na barra de busca (se houver)
    query = request.GET.get('q', '')

    # 2. Fazemos o filtro no banco de dados
    if query:
        # icontains = "contém" ignorando maiúsculas/minúsculas
        # A barra reta "|" significa "OU" (Busca no nome OU no SKU)
        produtos = Product.objects.filter(name__icontains=query) | Product.objects.filter(sku__icontains=query)
    else:
        # Se não tem busca, trazemos todos (Lembrando que o ActiveManager já esconde os inativos!)
        produtos = Product.objects.all()

    # 3. A MÁGICA DA RESPOSTA:
    # Se a requisição veio do HTMX (da barra de digitação)
    if request.headers.get('HX-Request'):
        return render(request, 'partials/produtos/_tabela.html', {'produtos': produtos})

    # Se foi um acesso normal (clicou no menu lateral)
    return render(request, 'produtos/lista.html', {'produtos': produtos})


# VIEW DE EDIÇÃO
def produto_editar_view(request, pk):
    # Buscamos o produto ou damos erro 404 se não existir
    produto = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Passamos a 'instance' para o Django saber que é uma atualização, não um novo cadastro
        form = ProductForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos:lista')
    else:
        form = ProductForm(instance=produto)
        
    return render(request, 'produtos/cadastro.html', {'form': form, 'produto': produto})

# VIEW DE EXCLUSÃO (SOFT DELETE)
@require_POST
def produto_deletar_view(request, pk):
    produto = get_object_or_404(Product, pk=pk)
    produto.is_active = False # Soft Delete
    produto.save()
    
    # Como o HTMX espera algo para colocar no lugar da linha, 
    # retornamos uma resposta vazia para a linha sumir
    return HttpResponse("")


@require_POST
def produto_bulk_deletar_view(request):
    # 1. Pegamos a lista de IDs que o HTMX 'pescou' dos checkboxes
    ids = request.POST.getlist('selected_ids')
    
    if ids:
        # 2. Fazemos o Soft Delete em massa usando o filtro __in
        Product.objects.filter(id__in=ids).update(is_active=False)
    
    # 3. Retornamos a tabela atualizada (sem os produtos deletados)
    produtos = Product.objects.all()
    return render(request, 'partials/produtos/_tabela.html', {'produtos': produtos})

# EXPORTAR PARA CSV
def produto_exportar_view(request):
    resource = ProductResource()
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produtos_exportados.csv"'
    return response

# IMPORTAR VIA CSV
def produto_importar_view(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        dataset = Dataset()
        novo_arquivo = request.FILES['arquivo']
        
        # Lemos o arquivo (assumindo CSV para simplificar)
        imported_data = dataset.load(novo_arquivo.read().decode('utf-8'), format='csv')
        resource = ProductResource()
        
        # Validamos os dados antes de salvar
        result = resource.import_data(dataset, dry_run=True)
        
        if not result.has_errors():
            resource.import_data(dataset, dry_run=False) # Salva de verdade
            return HttpResponse('<div class="alert alert-success">Importação concluída!</div>')
        else:
            return HttpResponse('<div class="alert alert-danger">Erro na importação. Verifique os dados.</div>')
            
    return render(request, 'partials/produtos/_modal_importar.html')