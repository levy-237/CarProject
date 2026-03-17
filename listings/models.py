from django.db import models
from cars.models import CarBrand,CarBodyType,CarModel,CarCondition,CarFuelType,CarTransmissionType
from django.utils import timezone

class Listing(models.Model):
    publish_date = models.DateField(default=timezone.now)
    brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    makeyear = models.DateField()
    price = models.IntegerField()
    body_type = models.ForeignKey(CarBodyType, on_delete=models.PROTECT)
    mileage = models.IntegerField()
    condition = models.ForeignKey(CarCondition, on_delete=models.PROTECT)
    power = models.IntegerField()
    fuel = models.ForeignKey(CarFuelType, on_delete=models.PROTECT)
    transmission = models.ForeignKey(CarTransmissionType, on_delete=models.PROTECT)
    is_online = models.BooleanField(default=False)
    