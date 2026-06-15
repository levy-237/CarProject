import factory
from factory.django import DjangoModelFactory

from users.models import User, Province, City


class ProvinceFactory(DjangoModelFactory):
    class Meta:
        model = Province

    name = factory.Sequence(lambda n: f"Province {n}")

class CityFactory(DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Sequence(lambda n: f"City {n}")
    province = factory.SubFactory(ProvinceFactory)

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpassword123")
    province = factory.SubFactory(ProvinceFactory)
    city = factory.SubFactory(CityFactory)
    is_private = False
