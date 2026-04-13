from django import forms

from produtos.models.product import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Quais campos queremos exibir na tela
        fields = [
            'category', 'sku', 'name', 'description', 'unit', 
            'cost_price', 'sale_price', 'current_stock', 'min_stock', 'low_stock_alert'
        ]

    # Técnica Avançada: Injetando o CSS do Bootstrap automaticamente em todos os campos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    # --- A CORREÇÃO DE ARQUITETURA AQUI ---
    def clean_sku(self):
        # 1. Pegamos o SKU que o usuário digitou na tela
        sku_digitado = self.cleaned_data.get('sku')
        
        # 2. Usamos o all_objects para procurar no banco INTEIRO (ativos e inativos)
        # Se for uma edição de produto, excluímos o próprio produto da busca para ele não dar erro com ele mesmo
        busca = Product.all_objects.filter(sku=sku_digitado)
        if self.instance and self.instance.pk:
            busca = busca.exclude(pk=self.instance.pk)
            
        # 3. Se achou alguém usando o SKU, barramos o formulário com educação
        if busca.exists():
            raise forms.ValidationError("Este SKU já está em uso (pode pertencer a um produto inativo).")
            
        return sku_digitado