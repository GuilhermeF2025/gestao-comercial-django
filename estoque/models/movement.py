from django.db import models
from django.conf import settings # <-- Importação corrigida
from produtos.models import Product

class StockMovement(models.Model):
    MOVEMENT_CHOICES = (
        ('IN', 'Entrada'),
        ('OUT', 'Saída'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements', verbose_name="Produto")
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES, verbose_name="Tipo")
    quantity = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Quantidade")
    reason = models.CharField(max_length=100, verbose_name="Motivo") 
    reference_document = models.CharField(max_length=50, blank=True, verbose_name="Doc. Referência") 
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")
    
    # <-- ForeignKey corrigida apontando para o settings
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Usuário"
    )

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"