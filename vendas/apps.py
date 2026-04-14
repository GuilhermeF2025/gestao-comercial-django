from django.apps import AppConfig

class VendasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendas'

    # Adicione esta função para carregar o Signal quando o servidor ligar
    def ready(self):
        import vendas.signals