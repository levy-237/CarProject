from django.db import models
from cars.models import CarBrand,CarBodyType,CarModel,CarCondition,CarFuelType,CarTransmissionType
from django.utils import timezone

class Listing(models.Model):
    publish_date = models.DateField(default=timezone.now)
    brand = models.ForeignKey(CarBrand, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True)
    makeyear = models.DateField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    body_type = models.ForeignKey(CarBodyType, on_delete=models.SET_NULL, null=True, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    condition = models.ForeignKey(CarCondition, on_delete=models.SET_NULL, null=True, blank=True)
    power = models.IntegerField(null=True, blank=True)
    fuel = models.ForeignKey(CarFuelType, on_delete=models.SET_NULL, null=True, blank=True)
    transmission = models.ForeignKey(CarTransmissionType, on_delete=models.SET_NULL, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    