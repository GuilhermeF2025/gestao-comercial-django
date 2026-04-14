from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Purchase
from estoque.models import StockMovement, StockBatch

@receiver(post_save, sender=Purchase)
def process_completed_purchase(sender, instance, **kwargs):
    # A mágica só acontece quando o dono da empresa muda o status para "CONCLUÍDA"
    if instance.status == 'COMPLETED':
        
        # Trava de Segurança: Verifica se já geramos os lotes dessa nota antes.
        if StockBatch.objects.filter(purchase=instance).exists():
            return
            
        # transaction.atomic garante que se der erro de energia no meio do processo, ele desfaz tudo.
        with transaction.atomic():
            for item in instance.items.all():
                produto = item.product
                
                # --- 1. MATEMÁTICA DO CUSTO MÉDICO PONDERADO ---
                estoque_antigo = produto.current_stock
                custo_medio_antigo = produto.average_cost
                
                valor_total_antigo = estoque_antigo * custo_medio_antigo
                valor_total_novo = item.quantity * item.unit_cost
                
                novo_estoque = estoque_antigo + item.quantity
                
                if novo_estoque > 0:
                    novo_custo_medio = (valor_total_antigo + valor_total_novo) / novo_estoque
                else:
                    novo_custo_medio = item.unit_cost

                # --- 2. GERAÇÃO DE HISTÓRICO (LIVRO RAZÃO) ---
                StockMovement.objects.create(
                    product=produto,
                    movement_type='IN',
                    quantity=item.quantity,
                    reason="Compra de Fornecedor",
                    reference_document=f"Compra #{instance.id}",
                    created_by=instance.created_by
                )

                # --- 3. GERAÇÃO DO LOTE FIFO (RECEITA FEDERAL) ---
                StockBatch.objects.create(
                    product=produto,
                    purchase=instance,
                    original_quantity=item.quantity,
                    current_quantity=item.quantity, # O lote nasce cheio
                    unit_cost=item.unit_cost
                )

                # --- 4. ATUALIZAÇÃO DO PRODUTO (GERENCIAL) ---
                produto.average_cost = novo_custo_medio
                produto.last_purchase_cost = item.unit_cost
                
                # Dica de Sênior: update_fields atualiza SÓ esses dois campos no banco,
                # para não correr o risco de sobrescrever o estoque que o StockMovement já alterou!
                produto.save(update_fields=['average_cost', 'last_purchase_cost'])