from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()