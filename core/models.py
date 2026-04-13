from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Nosso Usuário Customizado
class CustomUser(AbstractUser):
    # Definimos os perfis de acesso (RBAC - Role Based Access Control)
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('gerente', 'Gerente'),
        ('vendedor', 'Vendedor'),
        ('estoquista', 'Estoquista'),
    )
    
    # Adicionamos campos que o Django não tem por padrão
    cpf = models.CharField(max_length=14, blank=True, null=True, unique=True, verbose_name='CPF')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='vendedor', verbose_name='Perfil de Acesso')

    def __str__(self):
        # Como o usuário será exibido nos painéis (mostramos o nome de usuário e a regra)
        return f"{self.username} ({self.get_role_display()})"

# 2. Nossa Tabela de Auditoria Manual (Além do simple-history)
# Usada para registrar logins, logouts ou ações críticas do sistema.
class AuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"