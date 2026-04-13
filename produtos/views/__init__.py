# O ponto (.) no início significa "Importe desta mesma pasta"
from .lista import produto_lista_view
from .forms import produto_cadastro_view, produto_editar_view
from .acoes import produto_deletar_view, produto_bulk_deletar_view
from .importacao import produto_exportar_view, produto_importar_view

# Adicione esta linha importando todas as views de categorias:
from .categorias import *