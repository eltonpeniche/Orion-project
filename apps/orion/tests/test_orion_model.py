from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from .test_orion_base import OrionMixin


class OrionModelTest(TestCase,OrionMixin):
    def setUp(self):
       return super().setUp()
    
    def test_the_test(self):
        self.assertEqual(1, 1)

    @parameterized.expand([
        ('status_chamado', 1),
        ('numero_chamado', 14),
        ('descricao_chamado', 150),
        ('contato', 100),
    ])
    def test_chamado_fields_max_length(self, field, max_length):
        self.chamado = self.make_chamado()
        setattr(self.chamado, field, 'A' * (max_length +1))
        with self.assertRaises(ValidationError):
            self.chamado.full_clean()

    def test_chamado_status_chamado_is_aberto_by_default(self):
        self.chamado = self.make_chamado_default()
        self.assertEqual(self.chamado.status_chamado, 'A') 