from django import forms
from vendas.models import Sale, SaleItem

class PDVItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-select form-select-lg', 'autofocus': 'autofocus'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control form-control-lg', 'value': '1'})
        self.fields['quantity'].label = "Qtd."

class PDVCheckoutForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'payment_method']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-select form-select-lg'
        
        # O pagamento é obrigatório na hora de fechar a venda
        self.fields['payment_method'].required = True