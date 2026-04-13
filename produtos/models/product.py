from django.db import models
from core.managers import ActiveManager # Importamos o nosso filtro automático
from produtos.models.category import Category


class Product(models.Model):
    # Relacionamento de Categoria
    # PROTECT garante que a categoria não pode ser deletada se tiver produtos nela
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Categoria")
    
    sku = models.CharField(max_length=50, unique=True, verbose_name="Código SKU")
    name = models.CharField(max_length=200, verbose_name="Nome do Produto")
    description = models.TextField(blank=True, verbose_name="Descrição")
    unit = models.CharField(max_length=20, default='un', verbose_name="Unidade de Medida")
    
    # Valores Financeiros (decimal_places=4 é o padrão contábil)
    cost_price = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Preço de Custo")
    sale_price = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Preço de Venda")
    
    # Controle Físico
    current_stock = models.PositiveIntegerField(default=0, verbose_name="Estoque Atual")
    min_stock = models.PositiveIntegerField(default=5, verbose_name="Estoque Mínimo")
    low_stock_alert = models.PositiveIntegerField(default=10, verbose_name="Alerta de Estoque Baixo")
    
    # O nosso Soft Delete
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")

    # --- INJEÇÃO DOS MANAGERS ---
    # O 'objects' será o nosso manager padrão (só traz os ativos)
    objects = ActiveManager()
    # O 'all_objects' será um manager de backup para quando o admin precisar ver TUDO, inclusive os inativos
    all_objects = models.Manager() 

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.sku} - {self.name}"