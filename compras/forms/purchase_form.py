from django import forms
from compras.models import Purchase, PurchaseItem
import datetime

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'invoice_number', 'issue_date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['supplier'].widget.attrs['class'] = 'form-select'
        # Sugere a data de hoje automaticamente
        self.fields['issue_date'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}, 
            format='%Y-%m-%d'
        )
        if not self.instance.pk:
            self.initial['issue_date'] = datetime.date.today()

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'unit_cost']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['product'].widget.attrs['class'] = 'form-select'
        # Adiciona placeholders para guiar o usuário
        self.fields['quantity'].widget.attrs['placeholder'] = 'Ex: 10'
        self.fields['unit_cost'].widget.attrs['placeholder'] = 'Ex: 25.50'