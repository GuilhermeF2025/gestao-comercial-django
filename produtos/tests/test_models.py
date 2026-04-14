from django.test import TestCase
from django.db import IntegrityError
from produtos.models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        # O setUp roda antes de cada teste para criar um banco de dados temporário limpo.
        self.categoria = Category.objects.create(name="Eletrônicos", description="Teste")
        
        self.produto = Product.objects.create(
            category=self.categoria,
            sku="TEST-01",
            name="Mouse Sem Fio",
            cost_price=50.00,
            sale_price=100.00,
            current_stock=10
        )

    def test_produto_criado_com_sucesso(self):
        """Verifica se o produto foi salvo corretamente no banco"""
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.produto.name, "Mouse Sem Fio")

    def test_sku_deve_ser_unico(self):
        """Tentar criar um produto com SKU repetido deve gerar erro no banco"""
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                category=self.categoria,
                sku="TEST-01", # Usando o mesmo SKU de propósito
                name="Teclado",
                cost_price=10,
                sale_price=20
            )

    def test_manager_soft_delete_oculta_inativos(self):
        """Verifica se o ActiveManager esconde produtos com is_active=False"""
        # Simulamos o clique no botão de deletar (Soft Delete)
        self.produto.is_active = False
        self.produto.save()

        # O manager padrão NÃO deve enxergar o produto
        self.assertEqual(Product.objects.count(), 0)
        
        # Mas o all_objects (Auditoria) DEVE continuar enxergando
        self.assertEqual(Product.all_objects.count(), 1)