from rest_framework import serializers

from .models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarDriveTrain,
    CarModel,
    CarModelTrim
)


class CarBodyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBodyType
        fields = ["id", "name"]


class CarModelTrimSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModelTrim
        fields = ["id",
                  "name",
                  "max_ac_charge_kw",
                  "max_dc_charge_kw",
                  "twenty_to_eighty_charge_min",
                  ]

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


class CarBrandSerializer(serializers.ModelSerializer):
    models = CarModelSimpleSerializer(many=True, read_only=True)
    class Meta:
        model = CarBrand
        fields = ["id", 
                  "name",
                  "models",
                  ]
 
class CarModelSerializer(serializers.ModelSerializer):
    brand_detail = CarBrandSimpleSerializer(source="connected_brand", read_only=True)
    trims = CarModelTrimSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = CarModel
        fields = ["id",
                  "name",
                  "brand_detail",
                  "trims"          
                  ]


class CarModelTrimSerializer(serializers.ModelSerializer):
    connected_model_name = serializers.CharField(source="connected_model.name", read_only=True)
    drivetrain_name = serializers.CharField(source="drivetrain.name",read_only=True)
    class Meta:
        model = CarModelTrim
        fields = ["id",
                  "name",
                  "connected_model",
                  "connected_model_name",
                  "drivetrain_name",
                  "battery_size",
                  "drivetrain",
                  "factory_range",
                  "max_ac_charge_kw",
                  "max_dc_charge_kw",
                  "twenty_to_eighty_charge_min",
                ]



class CarDriveTrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDriveTrain
        fields = ["id", "name"]


class CarConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCondition
        fields = ["id", "name"]
