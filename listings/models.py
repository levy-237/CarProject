from django.db import models
from cars.models import CarBrand,CarBodyType,CarModel,CarCondition,CarFuelType,CarTransmissionType
from django.utils import timezone


def listing_image_upload_to(instance, filename):
    return f"listings/{instance.listing_id}/{filename}"


class Listing(models.Model):
    publish_date = models.DateField(auto_now_add=True)
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
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand} - {self.model} - {self.pk}"


class Image(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to=listing_image_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image #{self.pk} for listing #{self.listing_id}"