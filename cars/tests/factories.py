import factory
from factory.django import DjangoModelFactory

from cars.models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarFuelType,
    CarModel,
    CarTransmissionType,
)


class CarBodyTypeFactory(DjangoModelFactory):
    class Meta:
        model = CarBodyType

    name = factory.Sequence(lambda n: f"Body Type {n}")


class CarBrandFactory(DjangoModelFactory):
    class Meta:
        model = CarBrand

    name = factory.Sequence(lambda n: f"Brand {n}")


class CarModelFactory(DjangoModelFactory):
    class Meta:
        model = CarModel

    name = factory.Sequence(lambda n: f"Model {n}")
    connected_brand = factory.SubFactory(CarBrandFactory)


class CarConditionFactory(DjangoModelFactory):
    class Meta:
        model = CarCondition

    name = factory.Sequence(lambda n: f"Condition {n}")


class CarFuelTypeFactory(DjangoModelFactory):
    class Meta:
        model = CarFuelType

    name = factory.Sequence(lambda n: f"Fuel {n}")


class CarTransmissionTypeFactory(DjangoModelFactory):
    class Meta:
        model = CarTransmissionType

    name = factory.Sequence(lambda n: f"Transmission {n}")
