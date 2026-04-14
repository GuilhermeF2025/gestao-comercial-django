from django.db import models
from django.conf import settings
from clientes.models import Customer
from produtos.models import Product

class Sale(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Em Aberto (Caixa)'),
        ('COMPLETED', 'Finalizada (Baixa no Estoque)'),
        ('CANCELED', 'Cancelada'),
    )
    PAYMENT_CHOICES = (
        ('CASH', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CREDIT', 'Cartão de Crédito'),
        ('DEBIT', 'Cartão de Débito'),
    )

    # Cliente é opcional (null=True, blank=True) pois em PDV de balcão muita gente não informa CPF
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales', verbose_name="Cliente")
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, blank=True, null=True, verbose_name="Forma de Pagamento")
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total da Venda")

    # Auditoria
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-date_time', '-id']

    def __str__(self):
        return f"Venda #{self.id} - {self.get_status_display()}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produto")
    quantity = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Quantidade")
    
    # Preço cobrado do cliente na hora da venda
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço de Venda")
    
    # CMV (Custo da Mercadoria Vendida): Fotografado na hora para cálculo de lucro exato
    unit_cost = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Custo no Momento (CMV)")
    
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total do Item")

    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"

    def save(self, *args, **kwargs):
        # Se for um item novo (ainda não tem ID), nós "fotografamos" os valores do cadastro do produto
        if not self.pk:
            if not self.unit_price:
                self.unit_price = self.product.sale_price
            if not self.unit_cost:
                # O motor pega o custo médio exato que as compras calcularam
                self.unit_cost = self.product.average_cost 
                
        # Calcula o total final da linha
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
    @property
    def gross_profit(self):
        """Calcula o Lucro Bruto deste item em R$"""
        return self.total_price - (self.quantity * self.unit_cost)