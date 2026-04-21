from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from estoque.forms import StockMovementForm

# --- REGRA DE AUTORIZAÇÃO ---
def is_admin(user):
    return user.is_superuser

# --- A CEBOLA DE SEGURANÇA ---
@login_required
@user_passes_test(is_admin, login_url='/pdv/')
def ajuste_cadastro_view(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            
            # Como passamos pelo @login_required, temos 100% de certeza que o user existe
            movimentacao.created_by = request.user 
            movimentacao.save()
            
            return HttpResponse("""
            <div class="alert alert-success">✅ Movimentação registrada! O saldo do produto foi atualizado.</div>
            <button class="btn btn-primary mt-3" onclick="location.reload()">Atualizar Tela</button>
            """)
        return render(request, 'partials/estoque/_form.html', {'form': form})

    form = StockMovementForm()
    return render(request, 'partials/estoque/_form.html', {'form': form})