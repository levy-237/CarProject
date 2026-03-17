from django.db import models

class CarBodyType(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class CarBrand(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class CarModel(models.Model):
    name=models.CharField(max_length=100)
    connected_brand = models.ForeignKey(CarBrand,on_delete=models.SET_NULL,null=True,blank=True,related_name="models")
    def __str__(self):
        return self.name

class CarCondition(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class CarFuelType(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class CarTransmissionType(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
