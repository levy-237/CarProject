from django.db import models
from cars.models import CarBrand,CarBodyType,CarModel,CarCondition,CarFuelType,CarTransmissionType
from django.utils import timezone
from users.models import User

def listing_image_upload_to(instance, filename):
    return f"listings/{instance.listing_id}/{filename}"


class ListingsManager(models.Manager):
    def online(self):
        return self.filter(is_online=True)
    
    def premium(self):
        return self.filter(is_premium=True)
    
    def by_owner(self, user):
        return self.filter(owner=user)
    
    def not_hidden(self):
        return self.filter(hidden=False)
    
    def hidden(self):
        return self.filter(hidden=True)

    

class Province(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    

class City(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT,related_name="connected_cities")
    
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    publish_date = models.DateField(auto_now_add=True)
    title = models.TextField(max_length=2000)
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
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    description = models.TextField(max_length=2000)
    is_online = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    hidden = models.BooleanField(default=True)
    
    objects = ListingsManager()

    def __str__(self):
        return f"car listing id: {self.pk} \n owner: {self.owner.username} - {self.owner.id}"


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
    
    
class PriceHistory(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="price_history")
    old_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Price history for listing #{self.listing_id} at {self.created_at}"
    

