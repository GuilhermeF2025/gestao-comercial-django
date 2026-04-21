from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from compras.models import PurchaseRequest
from compras.forms import PurchaseRequestForm

@login_required
@permission_required('compras.view_purchaserequest', raise_exception=True)
def requisicao_lista_view(request):
    """Lista as solicitações. Estoquista vê as dele, Gerência vê todas."""
    
    # Se o usuário tem permissão de APROVAR (change), ele é chefe e vê tudo.
    if request.user.has_perm('compras.change_purchaserequest'):
        requisicoes = PurchaseRequest.objects.all()
    else:
        # Se for um reles mortal (Estoquista), vê só as que ele mesmo pediu.
        requisicoes = PurchaseRequest.objects.filter(requested_by=request.user)

    return render(request, 'compras/requisicoes_lista.html', {'requisicoes': requisicoes})


@login_required
@permission_required('compras.add_purchaserequest', raise_exception=True)
def requisicao_criar_view(request):
    """Tela onde o Estoquista faz o pedido"""
    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST)
        if form.is_valid():
            requisicao = form.save(commit=False)
            requisicao.requested_by = request.user # Assina o documento com o usuário logado
            requisicao.save()
            return redirect('compras:requisicao_lista')
    else:
        form = PurchaseRequestForm()
        
    return render(request, 'compras/requisicao_form.html', {'form': form})