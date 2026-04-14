from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Sale
from estoque.models import StockMovement, StockBatch

@receiver(post_save, sender=Sale)
def process_completed_sale(sender, instance, **kwargs):
    # A mágica só roda se o Caixa finalizou a venda e o cliente pagou
    if instance.status == 'COMPLETED':
        
        # Trava de Segurança: Evita abater o estoque duas vezes se a internet piscar
        if StockMovement.objects.filter(reference_document=f"Venda #{instance.id}").exists():
            return

        # transaction.atomic: Se der qualquer erro no meio do loop, o banco desfaz TUDO!
        with transaction.atomic():
            for item in instance.items.all():
                produto = item.product
                quantidade_necessaria = item.quantity

                # --- 1. O MOTOR FIFO (Consumindo Lotes Antigos) ---
                # Busca todos os lotes deste produto que ainda tem saldo, ordenados pela data (do mais velho pro mais novo)
                lotes_disponiveis = StockBatch.objects.filter(
                    product=produto,
                    current_quantity__gt=0
                ).order_by('created_at')

                for lote in lotes_disponiveis:
                    if quantidade_necessaria <= 0:
                        break # Já esvaziamos os lotes suficientes para cobrir a venda. Sai do loop.

                    if lote.current_quantity >= quantidade_necessaria:
                        # O lote tem o suficiente! Tiramos o que precisa e encerramos.
                        lote.current_quantity -= quantidade_necessaria
                        lote.save(update_fields=['current_quantity'])
                        quantidade_necessaria = 0
                    else:
                        # O lote não tem o suficiente! Esvaziamos ele e deixamos o loop ir pro próximo lote.
                        quantidade_necessaria -= lote.current_quantity
                        lote.current_quantity = 0
                        lote.save(update_fields=['current_quantity'])

                # Nota Sênior: Se ao final do loop 'quantidade_necessaria' for > 0, 
                # significa que o sistema vendeu algo que não tinha no estoque físico.
                # Nós vamos bloquear isso antes, na tela do PDV!

                # --- 2. GERAÇÃO DE HISTÓRICO E BAIXA FINAL ---
                # Criar esse movimento OUT dispara aquele outro signal do app 'estoque',
                # que vai abater o saldo total do 'current_stock' do Produto! Um dominó empurrando o outro.
                StockMovement.objects.create(
                    product=produto,
                    movement_type='OUT',
                    quantity=item.quantity,
                    reason="Venda PDV",
                    reference_document=f"Venda #{instance.id}",
                    created_by=instance.created_by
                )