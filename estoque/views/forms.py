from django.shortcuts import render
from django.http import HttpResponse
from estoque.forms import StockMovementForm

def ajuste_cadastro_view(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            # Injeta o usuário que está logado fazendo a ação
            if request.user.is_authenticated:
                movimentacao.created_by = request.user
            movimentacao.save()
            
            return HttpResponse("""
            <div class="alert alert-success">✅ Movimentação registrada! O saldo do produto foi atualizado.</div>
            <button class="btn btn-primary mt-3" onclick="location.reload()">Atualizar Tela</button>
            """)
        return render(request, 'partials/estoque/_form.html', {'form': form})

    form = StockMovementForm()
    return render(request, 'partials/estoque/_form.html', {'form': form})