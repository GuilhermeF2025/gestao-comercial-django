from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from produtos.models.product import Product

from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def produto_deletar_view(request, pk):
    produto = get_object_or_404(Product, pk=pk)
    produto.is_active = False
    produto.save()
    return HttpResponse("")


@login_required
@require_POST
def produto_bulk_deletar_view(request):
    ids = request.POST.getlist('selected_ids')
    if ids:
        Product.objects.filter(id__in=ids).update(is_active=False)
    
    produtos = Product.objects.all()
    return render(request, 'partials/produtos/_tabela.html', {'produtos': produtos})