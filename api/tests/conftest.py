import pytest
import factory
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Family, FamilyMembership, Gasto, Receita, MetaGasto


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    first_name = factory.Sequence(lambda n: f"User{n}")


class FamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Family

    name = factory.Sequence(lambda n: f"Family{n}")
    created_by = factory.SubFactory(UserFactory)


class FamilyMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FamilyMembership

    user = factory.SubFactory(UserFactory)
    family = factory.SubFactory(FamilyFactory)
    role = 'member'


class GastoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gasto

    user = factory.SubFactory(UserFactory)
    valor = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    categoria = factory.Iterator(['mercado', 'moradia', 'transporte', 'lazer'])
    descricao = factory.Faker('sentence')
    data = factory.LazyFunction(timezone.now)
    pago = False


class ReceitaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Receita

    user = factory.SubFactory(UserFactory)
    valor = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    descricao = factory.Faker('sentence')
    data = factory.LazyFunction(timezone.now)


class MetaGastoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MetaGasto

    user = factory.SubFactory(UserFactory)
    categoria = 'mercado'
    mes = factory.LazyFunction(lambda: timezone.now().month)
    ano = factory.LazyFunction(lambda: timezone.now().year)
    valor_meta = 1000.00


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client


@pytest.fixture
def family(user):
    family = FamilyFactory(created_by=user)
    FamilyMembershipFactory(user=user, family=family, role='admin')
    return family


@pytest.fixture
def gasto(user, family):
    return GastoFactory(user=user, family=family, valor=150.00, categoria='mercado', pago=True)


@pytest.fixture
def receita(user, family):
    return ReceitaFactory(user=user, family=family, valor=3000.00)


@pytest.fixture
def meta_gasto(user):
    return MetaGastoFactory(user=user, categoria='mercado', valor_meta=500.00)
