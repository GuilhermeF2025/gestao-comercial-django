from django import forms
from produtos.models.product import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'sku', 'name', 'description', 'unit', 
            'sale_price', 'average_cost', 'last_purchase_cost', 
            'current_stock', 'min_stock', 'low_stock_alert'
        ]
        
    # Técnica Avançada: Injetando o CSS e regras de interface
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Aplica o Bootstrap em todos os campos
        for field_name, field in self.fields.items():
            if field_name == 'category':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

        # 2. Bloqueia a edição manual dos custos (Eles serão geridos pelo App Compras)
        if 'average_cost' in self.fields:
            self.fields['average_cost'].widget.attrs['readonly'] = True
            self.fields['average_cost'].widget.attrs['style'] = 'background-color: #e9ecef; cursor: not-allowed;'
            
        if 'last_purchase_cost' in self.fields:
            self.fields['last_purchase_cost'].widget.attrs['readonly'] = True
            self.fields['last_purchase_cost'].widget.attrs['style'] = 'background-color: #e9ecef; cursor: not-allowed;'

    # --- A CORREÇÃO DE ARQUITETURA AQUI ---
    def clean_sku(self):
        # 1. Pegamos o SKU que o usuário digitou na tela
        sku_digitado = self.cleaned_data.get('sku')
        
        # 2. Usamos o all_objects para procurar no banco INTEIRO (ativos e inativos)
        busca = Product.all_objects.filter(sku=sku_digitado)
        if self.instance and self.instance.pk:
            busca = busca.exclude(pk=self.instance.pk)
            
        # 3. Se achou alguém usando o SKU, barramos o formulário com educação
        if busca.exists():
            raise forms.ValidationError("Este SKU já está em uso (pode pertencer a um produto inativo).")
            
        return sku_digitado