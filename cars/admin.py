from django.contrib import admin
from .models import CarBodyType,CarCondition,CarDriveTrain,CarModel,CarModelTrim,CarBrand

admin.site.register(CarBodyType)
admin.site.register(CarCondition)
admin.site.register(CarDriveTrain)
admin.site.register(CarModel)
admin.site.register(CarModelTrim)
admin.site.register(CarBrand)

# Register your models here.
