from django.db import models
from django.conf import settings
from produtos.models import Product

class PurchaseRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Aguardando Aprovação'),
        ('APPROVED', 'Aprovado (Liberado para Compra)'),
        ('REJECTED', 'Rejeitado pela Gerência'),
        ('COMPLETED', 'Atendido (Comprado)'), # Usado quando o Comprador finalizar o pedido
    )

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produto Solicitado")
    quantity = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Quantidade Necessária")
    justification = models.TextField(verbose_name="Justificativa / Observação")
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status da Solicitação")

    # --- RASTREABILIDADE (AUDITORIA) ---
    # Quem pediu (Estoquista)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
        related_name='requests_made', verbose_name="Solicitante"
    )
    # Quem aprovou ou rejeitou (Gerente)
    evaluated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='requests_evaluated', verbose_name="Avaliador"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Solicitação")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Solicitação de Compra"
        verbose_name_plural = "Solicitações de Compra"
        ordering = ['-created_at']

    def __str__(self):
        return f"Solicitação #{self.id} - {self.product.name} ({self.get_status_display()})"