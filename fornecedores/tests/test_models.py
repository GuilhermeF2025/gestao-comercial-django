from django.test import TestCase
from django.db import IntegrityError
from fornecedores.models import Supplier

class SupplierModelTest(TestCase):
    def setUp(self):
        self.fornecedor = Supplier.objects.create(
            name="Distribuidora XYZ",
            cnpj="00.000.000/0001-91"
        )

    def test_fornecedor_criado_com_sucesso(self):
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(self.fornecedor.name, "Distribuidora XYZ")

    def test_cnpj_deve_ser_unico(self):
        with self.assertRaises(IntegrityError):
            Supplier.objects.create(
                name="Outra Empresa",
                cnpj="00.000.000/0001-91" # Mesmo CNPJ
            )

    def test_manager_soft_delete_oculta_inativos(self):
        self.fornecedor.is_active = False
        self.fornecedor.save()
        self.assertEqual(Supplier.objects.count(), 0)
        self.assertEqual(Supplier.all_objects.count(), 1)