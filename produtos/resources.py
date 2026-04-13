from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from produtos.models import Product, Category

class ProductResource(resources.ModelResource):
    # Tratamento especial para a Categoria (buscar pelo nome na planilha)
    category = fields.Field(
        column_name='categoria',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )

    class Meta:
        model = Product
        # Campos que permitiremos importar/exportar
        fields = ('sku', 'name', 'category', 'unit', 'cost_price', 'sale_price', 'current_stock')
        # O SKU será nossa chave de busca para não duplicar itens na importação
        import_id_fields = ('sku',)
        skip_unchanged = True
        report_skipped = True