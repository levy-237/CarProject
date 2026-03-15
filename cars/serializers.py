from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.brand",read_only=True)
    model_name = serializers.CharField(source="model.model",read_only=True)
    body_type_name = serializers.CharField(source="body_type.body_type", read_only=True)
    condition_name = serializers.CharField(source="condition.condition", read_only=True)
    fuel_name = serializers.CharField(source="fuel.fuel_type", read_only=True)
    transmission_name = serializers.CharField(source="transmission.transmission_type", read_only=True)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = [
            "id",
            "url",
            "brand_name",
            "model_name",
            "makeyear",
            "price",
            "body_type_name",
            "mileage",
            "condition_name",
            "power",
            "fuel_name",
            "transmission_name",
            "is_online",
        ]
    
    def get_url(self,obj):
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("car-detail", kwargs={"pk": obj.pk}, request=request)