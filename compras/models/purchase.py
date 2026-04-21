from django.db import models
from django.conf import settings
from fornecedores.models import Supplier
from produtos.models import Product

class Purchase(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendente (Em cotação / Aguardando entrega)'),
        ('COMPLETED', 'Concluída (Recebida e Estoque Atualizado)'),
        ('CANCELED', 'Cancelada'),
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchases', verbose_name="Fornecedor")
    invoice_number = models.CharField(max_length=50, blank=True, verbose_name="Número da Nota (NF-e)")
    issue_date = models.DateField(verbose_name="Data de Emissão")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    
    # Valores totais caculados
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Valor Total")

    # Auditoria
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Comprador")

    class Meta:
        verbose_name = "Pedido de Compra" # Atualizado para a nova nomenclatura
        verbose_name_plural = "Pedidos de Compra"
        ordering = ['-issue_date', '-id']

    def __str__(self):
        return f"Pedido #{self.id} - {self.supplier.name}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produto")
    
    # --- A MÁGICA DA AUDITORIA AQUI (O Fio Condutor) ---
    # Liga o item comprado à solicitação original feita pelo estoquista.
    # É null=True e blank=True para permitir que o comprador faça compras diretas emergenciais se precisar.
    origin_request = models.ForeignKey(
        'compras.PurchaseRequest', 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='purchase_items', 
        verbose_name="Solicitação de Origem"
    )
    
    quantity = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Quantidade")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Custo Unitário")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Custo Total")

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def save(self, *args, **kwargs):
        # Calcula o total da linha automaticamente antes de salvar
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)