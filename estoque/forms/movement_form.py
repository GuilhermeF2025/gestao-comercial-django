from django import forms
from estoque.models import StockMovement

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reason', 'reference_document']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        # Facilitando a vida do usuário com valores padrão sugeridos
        self.fields['reason'].initial = 'Ajuste Manual'

    def clean_quantity(self):
        quantidade = self.cleaned_data.get('quantity')
        if quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantidade