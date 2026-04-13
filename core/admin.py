from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AuditLog

# Personalizamos a tela de edição do usuário no painel Admin
class CustomUserAdmin(UserAdmin):
    # Adicionamos nossos campos customizados na tela de detalhes
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais (SaaS)', {'fields': ('cpf', 'phone', 'role')}),
    )
    # Adicionamos nossos campos na lista de visualização em tabela
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')

# Registramos os modelos no painel
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AuditLog)