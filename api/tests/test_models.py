from django.test import TestCase
from api.models import Gasto


class GastoModelTests(TestCase):
    def test_criar_gasto(self):
        gasto = Gasto.objects.create(
            valor=100.50,
            categoria='alimentacao',
            descricao='Almoço',
        )
        self.assertEqual(gasto.valor, 100.50)
        self.assertEqual(gasto.categoria, 'alimentacao')
