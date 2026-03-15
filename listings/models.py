from django.db import models
from cars.models import Car

class Listing(models.Model):
    publish_date = models.DateField()
    car = models.ForeignKey(Car,on_delete=models.SET_NULL,null=True)
    