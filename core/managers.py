from django.db import models

class ActiveManager(models.Manager):
    """
    Este manager altera o comportamento padrão do Django.
    Quando chamarmos Model.objects.all(), ele trará APENAS
    os registros onde is_active for True.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)