import factory
from factory.django import DjangoModelFactory

from cars.models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarDriveTrain,
    CarModel,
    CarModelTrim,
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

class CarDriveTrainFactory(DjangoModelFactory):
    class Meta:
        model = CarDriveTrain

    name = factory.Sequence(lambda n: f"Drive Train {n}")

class CarModelTrimFactory(DjangoModelFactory):
    class Meta:
        model = CarModelTrim

    name = factory.Sequence(lambda n: f"Model Trim {n}")
    connected_model = factory.SubFactory(CarModelFactory)
    battery_size = 100
    drivetrain = factory.SubFactory(CarDriveTrainFactory)
    factory_range = 100
    max_ac_charge_kw = 100
    max_dc_charge_kw = 100
    twenty_to_eighty_charge_min = 100

class CarConditionFactory(DjangoModelFactory):
    class Meta:
        model = CarCondition

    name = factory.Sequence(lambda n: f"Condition {n}")


