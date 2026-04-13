from django import forms
from fornecedores.models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'cnpj', 'phone', 'email', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    def clean_cnpj(self):
        cnpj_digitado = self.cleaned_data.get('cnpj')
        busca = Supplier.all_objects.filter(cnpj=cnpj_digitado)
        
        if self.instance and self.instance.pk:
            busca = busca.exclude(pk=self.instance.pk)
            
        if busca.exists():
            raise forms.ValidationError("Este CNPJ já está cadastrado.")
        return cnpj_digitado