from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockMovement

@receiver(post_save, sender=StockMovement)
def update_product_stock(sender, instance, created, **kwargs):
    """
    Toda vez que uma movimentação é salva (created=True),
    esta função pega o produto associado e atualiza o saldo.
    """
    if created:
        produto = instance.product
        
        if instance.movement_type == 'IN':
            produto.current_stock += instance.quantity
        elif instance.movement_type == 'OUT':
            produto.current_stock -= instance.quantity
            
        produto.save()