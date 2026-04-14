from django.test import TestCase, Client
from django.urls import reverse
from clientes.models import Customer

class CustomerViewTest(TestCase):
    def setUp(self):
        # self.client é um "Navegador Fantasma". Ele simula cliques e acessos
        # a URLs sem precisar abrir o Chrome de verdade.
        self.client = Client()
        
        # Criamos um cliente falso para testarmos a tabela
        self.cliente = Customer.objects.create(
            name="João Silva",
            cpf_cnpj="123.456.789-00"
        )

    # -------------------------------------------------------------------------
    # TESTE 1: ACESSO PELO MENU (PÁGINA COMPLETA)
    # Objetivo: Se eu digitar /clientes/ no navegador, deve carregar o menu lateral
    # e a página inteira (base.html).
    # -------------------------------------------------------------------------
    def test_lista_clientes_acesso_normal(self):
        # reverse() converte o nome da URL ('clientes:lista') no link real ('/clientes/')
        response = self.client.get(reverse('clientes:lista'))
        
        # status_code 200 significa "Página encontrada com sucesso" (OK)
        self.assertEqual(response.status_code, 200)
        # Verifica se o Django usou o 'base.html' para montar a página
        self.assertTemplateUsed(response, 'base.html')

    # -------------------------------------------------------------------------
    # TESTE 2: ACESSO PELA BARRA DE BUSCA (HTMX)
    # Objetivo: Se a requisição vier do HTMX, NÃO deve carregar o menu lateral
    # (base.html), deve devolver apenas o pedaço da tabela (_tabela.html).
    # -------------------------------------------------------------------------
    def test_lista_clientes_requisicao_htmx(self):
        # HTTP_HX_REQUEST='true' é o crachá que o HTMX mostra para o servidor
        response = self.client.get(reverse('clientes:lista'), HTTP_HX_REQUEST='true')
        
        self.assertEqual(response.status_code, 200)
        # Afirma que usou a tabela parcial
        self.assertTemplateUsed(response, 'partials/clientes/_tabela.html')
        # Afirma que NÃO usou a base (Economia de internet do usuário)
        self.assertTemplateNotUsed(response, 'base.html')

    # -------------------------------------------------------------------------
    # TESTE 3: VALIDAÇÃO DE FORMULÁRIO (CPF REPETIDO)
    # Objetivo: Se um usuário preencher o formulário com um CPF que já existe,
    # o sistema deve devolver a tela com a mensagem de erro.
    # -------------------------------------------------------------------------
    def test_cadastro_cliente_cpf_duplicado(self):
        # Criamos um dicionário simulando os campos preenchidos na tela
        dados_form = {
            'name': 'Carlos Silva',
            'cpf_cnpj': '123.456.789-00', # CPF do João que criamos no setUp
            'phone': '',
            'email': '',
            'address': ''
        }
        
        # Simulamos o clique no botão "Salvar" (POST)
        response = self.client.post(reverse('clientes:cadastro'), data=dados_form)
        
        self.assertEqual(response.status_code, 200)
        # assertContains procura um texto exato dentro do HTML que o servidor devolveu
        self.assertContains(response, 'Este CPF/CNPJ já está cadastrado no sistema.')

    # -------------------------------------------------------------------------
    # TESTE 4: AÇÃO DO BOTÃO DELETAR (HTMX)
    # Objetivo: Clicar no botão da lixeira deve desativar o cliente e devolver
    # um texto vazio para a linha da tabela desaparecer da tela.
    # -------------------------------------------------------------------------
    def test_soft_delete_view_htmx(self):
        # Enviamos um POST para a URL de deletar passando o ID do João
        response = self.client.post(reverse('clientes:deletar', args=[self.cliente.id]))
        
        self.assertEqual(response.status_code, 200)
        # b'' significa byte vazio. É o HTML vazio que mandamos o HTMX injetar.
        self.assertEqual(response.content, b'') 
        
        # Vamos no banco de dados "acordar" o cliente para ver o que aconteceu com ele
        self.cliente.refresh_from_db()
        # Afirma que a flag "is_active" agora é Falsa.
        self.assertFalse(self.cliente.is_active)