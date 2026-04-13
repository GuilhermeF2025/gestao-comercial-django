from django import forms
from clientes.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'cpf_cnpj', 'phone', 'email', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicando Bootstrap em todos os campos automaticamente
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    def clean_cpf_cnpj(self):
        # Proteção: Verifica se o CPF/CNPJ já existe até mesmo nos inativos
        documento = self.cleaned_data.get('cpf_cnpj')
        busca = Customer.all_objects.filter(cpf_cnpj=documento)
        
        if self.instance and self.instance.pk:
            busca = busca.exclude(pk=self.instance.pk)
            
        if busca.exists():
            raise forms.ValidationError("Este CPF/CNPJ já está cadastrado no sistema.")
        return documento