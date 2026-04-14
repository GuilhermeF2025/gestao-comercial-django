from django.test import TestCase, Client
from django.urls import reverse
from fornecedores.models import Supplier

class SupplierViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.fornecedor = Supplier.objects.create(
            name="Distribuidora XYZ",
            cnpj="00.000.000/0001-91"
        )

    def test_lista_fornecedores_acesso_normal(self):
        response = self.client.get(reverse('fornecedores:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_lista_fornecedores_requisicao_htmx(self):
        response = self.client.get(reverse('fornecedores:lista'), HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/fornecedores/_tabela.html')
        self.assertTemplateNotUsed(response, 'base.html')

    def test_cadastro_fornecedor_cnpj_duplicado(self):
        dados_form = {
            'name': 'Nova Empresa',
            'cnpj': '00.000.000/0001-91', # CNPJ repetido
            'phone': '',
            'email': '',
            'address': ''
        }
        response = self.client.post(reverse('fornecedores:cadastro'), data=dados_form)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este CNPJ já está cadastrado.')

    def test_soft_delete_view_htmx(self):
        response = self.client.post(reverse('fornecedores:deletar', args=[self.fornecedor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'') 
        self.fornecedor.refresh_from_db()
        self.assertFalse(self.fornecedor.is_active)