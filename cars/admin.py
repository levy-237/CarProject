from django.contrib import admin
from .models import CarBodyType,CarCondition,CarFuelType,CarTransmissionType,CarModel,CarBrand

admin.site.register(CarBodyType)
admin.site.register(CarCondition)
admin.site.register(CarFuelType)
admin.site.register(CarTransmissionType)
admin.site.register(CarModel)
admin.site.register(CarBrand)

# Register your models here.
