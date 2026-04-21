from .lista import compra_lista_view
from .pedido import compra_criar_view, compra_detalhe_view
from .itens import adicionar_item_view, remover_item_view
from .acoes import finalizar_compra_view
from .requisicao import requisicao_lista_view, requisicao_criar_view # <-- Adicione esta linha
from .gerencia import requisicoes_pendentes_view, avaliar_requisicao_view
from .comprador import painel_comprador_view, iniciar_compra_da_solicitacao