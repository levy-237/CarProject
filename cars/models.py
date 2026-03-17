from django.db import models

class CarBodyType(models.Model):
    body_type=models.CharField(max_length=100)
    def __str__(self):
        return self.body_type
    
class CarBrand(models.Model):
    brand=models.CharField(max_length=100)
    def __str__(self):
        return self.brand

class CarModel(models.Model):
    model=models.CharField(max_length=100)
    connected_brand = models.ForeignKey(CarBrand,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.model

class CarCondition(models.Model):
    condition=models.CharField(max_length=100)
    def __str__(self):
        return self.condition
    
class CarFuelType(models.Model):
    fuel_type=models.CharField(max_length=100)
    def __str__(self):
        return self.fuel_type
    
class CarTransmissionType(models.Model):
    transmission_type=models.CharField(max_length=100)
    def __str__(self):
        return self.transmission_type
    
