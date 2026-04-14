from django.apps import AppConfig

class EstoqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estoque'

    # Adicione esta função para carregar os Signals quando o app ligar
    def ready(self):
        import estoque.signals