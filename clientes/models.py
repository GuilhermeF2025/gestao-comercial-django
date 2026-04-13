from django.db import models
from core.managers import ActiveManager

class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome Completo / Razão Social")
    # CPF/CNPJ juntos pois um cliente pode ser pessoa física ou jurídica
    cpf_cnpj = models.CharField(max_length=18, unique=True, verbose_name="CPF ou CNPJ")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    address = models.TextField(blank=True, verbose_name="Endereço Completo")
    
    # Nosso Soft Delete
    is_active = models.BooleanField(default=True, verbose_name="Ativo?")

    # Injetando os Managers
    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.name} - {self.cpf_cnpj}"