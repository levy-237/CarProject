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
    connected_brand = models.ForeignKey(CarBrand,on_delete=models.CASCADE,related_name="models")
    def __str__(self):
        return self.name

class CarDriveTrain(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name


class CarCondition(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class CarModelTrim(models.Model):
    name = models.CharField(max_length=100)
    connected_model = models.ForeignKey(CarModel,on_delete=models.CASCADE,related_name="trims")
    battery_size = models.IntegerField(null=True,blank=True)
    drivetrain = models.ForeignKey(CarDriveTrain, on_delete=models.PROTECT,null=True,blank=True)
    factory_range = models.IntegerField(null=True,blank=True)
    max_ac_charge_kw = models.FloatField(null=True, blank=True)
    max_dc_charge_kw = models.FloatField(null=True, blank=True)
    twenty_to_eighty_charge_min = models.IntegerField(null=True, blank=True)
    
    
    def __str__(self):
        return self.name
    
    
