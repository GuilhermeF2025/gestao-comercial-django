from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'sale_price', 'current_stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('sku', 'name')
    list_editable = ('sale_price', 'is_active') # Permite editar o preço e status direto na tabela