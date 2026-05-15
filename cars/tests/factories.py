import factory
from factory.django import DjangoModelFactory

from cars.models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarDriveTrain,
    CarModel,
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


class CarDriveTrainFactory(DjangoModelFactory):
    class Meta:
        model = CarDriveTrain

    name = factory.Sequence(lambda n: f"Drive Train {n}")
