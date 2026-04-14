from django.db import models
from produtos.models import Product

class StockBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batches', verbose_name="Produto")
    # Usamos string 'compras.Purchase' para evitar erro de importação circular
    purchase = models.ForeignKey('compras.Purchase', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Compra Origem")
    
    original_quantity = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Qtd Original")
    current_quantity = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Qtd Atual")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Custo Unitário")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lote de Estoque"
        verbose_name_plural = "Lotes de Estoque"
        ordering = ['created_at'] # A MAGIA DO FIFO AQUI: O mais antigo aparece primeiro!

    def __str__(self):
        return f"Lote {self.id} - {self.product.name} ({self.current_quantity} restantes)"