from django.contrib import admin
from estoque.models import StockMovement

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'product', 'movement_type', 'quantity', 'reason', 'created_by')
    list_filter = ('movement_type', 'created_at', 'reason')
    search_fields = ('product__name', 'reference_document')
    # Proteção de Auditoria: Movimentações nunca devem ser alteradas manualmente no admin!
    readonly_fields = ('product', 'movement_type', 'quantity', 'reason', 'reference_document', 'created_by', 'created_at')

    def has_add_permission(self, request):
        return False # Desabilita adicionar pelo Admin nativo para forçar o uso do nosso sistema