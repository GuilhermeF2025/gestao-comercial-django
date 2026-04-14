from django.db import models
from django.conf import settings
from fornecedores.models import Supplier
from produtos.models import Product

class Purchase(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendente'),
        ('COMPLETED', 'Concluída (Estoque Atualizado)'),
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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-issue_date', '-id']

    def __str__(self):
        return f"Compra #{self.id} - {self.supplier.name}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produto")
    quantity = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Quantidade")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Custo Unitário")
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Custo Total")

    class Meta:
        verbose_name = "Item da Compra"
        verbose_name_plural = "Itens da Compra"

    def save(self, *args, **kwargs):
        # Calcula o total da linha automaticamente antes de salvar
        self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)