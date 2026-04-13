from django.db import models
from core.managers import ActiveManager

class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Razão Social / Nome Fantasia")
    # Fornecedores de ERP geralmente são apenas Pessoa Jurídica
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    address = models.TextField(blank=True, verbose_name="Endereço Completo")
    
    # Nosso Soft Delete
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")

    # Injetando os Managers
    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.name