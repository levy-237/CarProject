from rest_framework import serializers

from .models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarFuelType,
    CarModel,
    CarTransmissionType,
)


class CarBodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBodyType
        fields = ["id", "name"]


class CarModelSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ["id",
                  "name",
                  ]




class CarBrandSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ["id", 
                  "name",
                  ]
    
class CarModelSerializer(serializers.ModelSerializer):
    brand_detail = CarBrandSimpleSerializer(source="connected_brand", read_only=True)
    class Meta:
        model = CarModel
        fields = ["id",
                  "name",
                  "brand_detail",          
                  ]

class CarBrandSerializer(serializers.ModelSerializer):
    models = CarModelSimpleSerializer(many=True, read_only=True)
    class Meta:
        model = CarBrand
        fields = ["id", 
                  "name",
                  "models"
                  ]


class CarConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCondition
        fields = ["id", "name"]


class CarFuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFuelType
        fields = ["id", "name"]


class CarTransmissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarTransmissionType
        fields = ["id", "name"]
