from django import forms
from compras.models import PurchaseRequest

class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['product', 'quantity', 'justification']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['product'].widget.attrs['class'] = 'form-select'
        self.fields['justification'].widget.attrs['rows'] = 3
        self.fields['justification'].widget.attrs['placeholder'] = 'Ex: Estoque mínimo atingido. Previsão de alta demanda no próximo mês.'