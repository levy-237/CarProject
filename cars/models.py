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
    
class Car(models.Model):
    brand = models.ForeignKey(CarBrand,on_delete=models.SET_NULL,null=True)
    model = models.ForeignKey(CarModel,on_delete=models.SET_NULL,null=True)
    makeyear = models.DateField()
    price = models.IntegerField()
    body_type = models.ForeignKey(CarBodyType,on_delete=models.SET_NULL,null=True)
    mileage = models.IntegerField()
    condition = models.ForeignKey(CarCondition,on_delete=models.SET_NULL,null=True)
    power = models.IntegerField()
    fuel =  models.ForeignKey(CarFuelType,on_delete=models.SET_NULL,null=True)
    transmission = models.ForeignKey(CarTransmissionType,on_delete=models.SET_NULL,null=True)
    is_online = models.BooleanField(default=False)
    