import factory
from factory.django import DjangoModelFactory
from datetime import date

from listings.models import Listing, Image
from users.tests.factories import UserFactory
from cars.tests.factories import (
    CarBodyTypeFactory,
    CarBrandFactory,
    CarConditionFactory,
    CarModelFactory,
    CarModelTrimFactory,
    CarBodyTypeFactory,
)

class ListingFactory(DjangoModelFactory):
    class Meta:
        model = Listing

    owner = factory.SubFactory(UserFactory)
    brand = factory.SubFactory(CarBrandFactory)
    model = factory.SubFactory(CarModelFactory, connected_brand=factory.SelfAttribute("..brand"))
    model_trim = factory.SubFactory(CarModelTrimFactory, connected_model=factory.SelfAttribute("..model"))
    condition = factory.SubFactory(CarConditionFactory)
    body_type = factory.SubFactory(CarBodyTypeFactory)
    makeyear = date(2020, 1, 1)
    price = 25000
    mileage = 10000
    power = 150
    is_online = True
    is_premium = False
    is_under_review = False
    description = "This is a test listing"


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    listing = factory.SubFactory(ListingFactory)
    image = factory.Sequence(lambda n: f"https://cdn.example.com/image-{n}.jpg")
    storage_key = factory.Sequence(lambda n: f"storage-key-{n}")
    is_cover = False