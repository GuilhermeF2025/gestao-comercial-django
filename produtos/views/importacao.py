import csv
from django.http import HttpResponse
from django.shortcuts import render
from tablib import Dataset
from produtos.resources import ProductResource

def produto_exportar_view(request):
    resource = ProductResource()
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produtos_exportados.csv"'
    return response

def produto_importar_view(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        dataset = Dataset()
        novo_arquivo = request.FILES['arquivo']
        
        imported_data = dataset.load(novo_arquivo.read().decode('utf-8'), format='csv')
        resource = ProductResource()
        result = resource.import_data(dataset, dry_run=True)
        
        if not result.has_errors():
            resource.import_data(dataset, dry_run=False)
            return HttpResponse('<div class="alert alert-success">Importação concluída! 🚀 Atualize a página.</div>')
        else:
            return HttpResponse('<div class="alert alert-danger">Erro na importação. Verifique os dados do arquivo.</div>')
            
    return render(request, 'partials/produtos/_modal_importar.html')