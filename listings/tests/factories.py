import factory
from factory.django import DjangoModelFactory
from datetime import date

from listings.models import Listing
from users.tests.factories import UserFactory
from cars.tests.factories import (
    CarBodyTypeFactory,
    CarBrandFactory,
    CarConditionFactory,
    CarDriveTrainFactory,
    CarModelFactory,
)

class ListingFactory(DjangoModelFactory):
    class Meta:
        model = Listing

    owner = factory.SubFactory(UserFactory)
    brand = factory.SubFactory(CarBrandFactory)
    model = factory.SubFactory(CarModelFactory, connected_brand=factory.SelfAttribute("..brand"))
    body_type = factory.SubFactory(CarBodyTypeFactory)
    condition = factory.SubFactory(CarConditionFactory)
    drivetrain = factory.SubFactory(CarDriveTrainFactory)
    makeyear = date(2020, 1, 1)
    price = 25000
    mileage = 10000
    power = 150
    is_online = True
    is_premium = False
    hidden = False