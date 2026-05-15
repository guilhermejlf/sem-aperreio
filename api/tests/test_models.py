import pytest
from django.contrib.auth.models import User
from api.models import Family, FamilyMembership, Gasto, Receita, MetaGasto


@pytest.mark.django_db
class TestGastoModel:
    def test_criar_gasto(self, user):
        gasto = Gasto.objects.create(
            user=user,
            valor=100.50,
            categoria='mercado',
            descricao='Almoço',
            data='2024-05-15',
        )
        assert gasto.valor == 100.50
        assert gasto.categoria == 'mercado'
        assert 'Mercado' in str(gasto)
        assert '100.5' in str(gasto)

    def test_gasto_valor_negativo(self, user):
        from django.core.exceptions import ValidationError
        gasto = Gasto(user=user, valor=-10, categoria='mercado', data='2024-05-15')
        with pytest.raises(ValidationError):
            gasto.full_clean()


@pytest.mark.django_db
class TestReceitaModel:
    def test_criar_receita(self, user):
        receita = Receita.objects.create(
            user=user,
            valor=3000.00,
            descricao='Salário',
            data='2024-05-01',
        )
        assert receita.valor == 3000.00
        assert 'R$ 3000' in str(receita)
        assert 'Salário' in str(receita)


@pytest.mark.django_db
class TestFamilyModel:
    def test_criar_family(self, user):
        family = Family.objects.create(name='Família Teste', created_by=user)
        assert len(family.code) == 6
        assert family.code.isalnum()

    def test_regenerate_code(self, user):
        family = Family.objects.create(name='Teste', created_by=user)
        old_code = family.code
        family.regenerate_code()
        assert family.code != old_code
        assert len(family.code) == 6


@pytest.mark.django_db
class TestFamilyMembershipModel:
    def test_membership_role(self, user, family):
        assert FamilyMembership.objects.filter(user=user, family=family).exists()


@pytest.mark.django_db
class TestMetaGastoModel:
    def test_criar_meta(self, user):
        meta = MetaGasto.objects.create(
            user=user,
            categoria='mercado',
            mes=5,
            ano=2024,
            valor_meta=500.00,
        )
        assert meta.valor_meta == 500.00
        assert 'Meta Mercado' in str(meta)
        assert '500' in str(meta)

    def test_meta_geral(self, user):
        meta = MetaGasto.objects.create(
            user=user,
            categoria=None,
            mes=5,
            ano=2024,
            valor_meta=2000.00,
        )
        assert 'Meta Geral' in str(meta)
        assert '2000' in str(meta)
