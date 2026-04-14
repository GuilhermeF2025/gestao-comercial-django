from django.test import TestCase
from django.db import IntegrityError
from clientes.models import Customer

class CustomerModelTest(TestCase):
    # -------------------------------------------------------------------------
    # 1. SETUP: PREPARANDO O TERRENO
    # O método setUp roda ANTES de cada um dos testes abaixo.
    # O Django cria um banco de dados falso e vazio. Aqui nós colocamos
    # dados nesse banco falso para os testes poderem brincar com eles.
    # -------------------------------------------------------------------------
    def setUp(self):
        self.cliente = Customer.objects.create(
            name="João Silva",
            cpf_cnpj="123.456.789-00",
            email="joao@teste.com"
        )

    # -------------------------------------------------------------------------
    # 2. TESTE DE CRIAÇÃO BÁSICA
    # Objetivo: Garantir que o banco de dados está salvando as informações.
    # -------------------------------------------------------------------------
    def test_cliente_criado_com_sucesso(self):
        # assertEqual(A, B) -> Verifica se A é igual a B.
        # Estamos perguntando: "A contagem de clientes no banco é 1?"
        self.assertEqual(Customer.objects.count(), 1)
        # Estamos perguntando: "O nome do cliente salvo é 'João Silva'?"
        self.assertEqual(self.cliente.name, "João Silva")

    # -------------------------------------------------------------------------
    # 3. TESTE DE REGRA DE NEGÓCIO (CPF ÚNICO)
    # Objetivo: Garantir que o banco não aceite CPFs iguais.
    # -------------------------------------------------------------------------
    def test_cpf_cnpj_deve_ser_unico(self):
        # assertRaises(Erro) -> Diz ao teste: "O próximo comando DEVE dar erro".
        # Se não der erro, o teste falha (pois aceitou dado duplicado).
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                name="Maria Souza",
                cpf_cnpj="123.456.789-00" # Tentando salvar o CPF do João
            )

    # -------------------------------------------------------------------------
    # 4. TESTE DA AUDITORIA (SOFT DELETE)
    # Objetivo: Garantir que apagar um cliente apenas o esconde, não o destrói.
    # -------------------------------------------------------------------------
    def test_manager_soft_delete_oculta_inativos(self):
        # Simulamos a ação de deletar mudando a flag para False
        self.cliente.is_active = False
        self.cliente.save()

        # O manager padrão (objects) filtra os ativos, então deve ver ZERO clientes.
        self.assertEqual(Customer.objects.count(), 0)
        
        # O manager de auditoria (all_objects) vê tudo, então DEVE ver 1 cliente.
        self.assertEqual(Customer.all_objects.count(), 1)