from django.test import TestCase, Client
from django.urls import reverse
from produtos.models import Product, Category

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client() # Simula um navegador de internet
        self.categoria = Category.objects.create(name="Geral")
        self.produto = Product.objects.create(
            category=self.categoria, 
            sku="SKU-TESTE", 
            name="Monitor", 
            cost_price=100, 
            sale_price=200
        )

    def test_lista_produtos_acesso_normal(self):
        """Acesso via URL normal deve retornar a página HTML completa"""
        response = self.client.get(reverse('produtos:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produtos/lista.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_lista_produtos_requisicao_htmx(self):
        """Acesso via barra de busca (HTMX) deve retornar APENAS a tabela"""
        # Simulamos o cabeçalho invisível que o HTMX envia
        response = self.client.get(reverse('produtos:lista'), HTTP_HX_REQUEST='true')
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/produtos/_tabela.html')
        # Garante que o base.html NÃO foi carregado junto
        self.assertTemplateNotUsed(response, 'base.html')

    def test_cadastro_produto_sku_duplicado(self):
        """O formulário deve barrar o cadastro se o SKU já existir e devolver a tela com erro"""
        dados_form = {
            'category': self.categoria.id,
            'sku': 'SKU-TESTE', # Tentando cadastrar o mesmo SKU do setUp
            'name': 'Outro Monitor',
            'unit': 'un',             # <-- Faltavam estes campos obrigatórios!
            'cost_price': 10,
            'sale_price': 20,
            'current_stock': 5,
            'min_stock': 1,           # <-- Faltavam estes campos obrigatórios!
            'low_stock_alert': 2      # <-- Faltavam estes campos obrigatórios!
        }
        
        response = self.client.post(reverse('produtos:cadastro'), data=dados_form)
        
        # O Django deve devolver 200 OK, mas com o formulário inválido
        self.assertEqual(response.status_code, 200)
        
        # É mais seguro buscar pelo texto exato do erro do que pela classe CSS
        self.assertContains(response, 'Este SKU já está em uso')

    def test_soft_delete_view_htmx(self):
        """Testa se o botão de lixeira desativa o produto e retorna HTML vazio para sumir da tela"""
        response = self.client.post(reverse('produtos:deletar', args=[self.produto.id]))
        
        # O HTMX espera 200 OK
        self.assertEqual(response.status_code, 200)
        
        # A view deve retornar VAZIO para que a linha da tabela desapareça
        self.assertEqual(response.content, b'') 
        
        # Verifica no banco de dados se a flag foi alterada para False
        self.produto.refresh_from_db()
        self.assertFalse(self.produto.is_active)