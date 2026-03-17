from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Listing
from cars.serializers import CarBrandSimpleSerializer,CarModelSimpleSerializer,CarConditionSerializer,CarTransmissionTypeSerializer,CarBodyTypeSerializer,CarFuelTypeSerializer

class ListingSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    brand_detail = CarBrandSimpleSerializer(source="brand", read_only=True)
    model_detail = CarModelSimpleSerializer(source="model", read_only=True)
    condition_detail = CarConditionSerializer(source="condition", read_only=True)
    transmission_detail = CarTransmissionTypeSerializer(source="transmission", read_only=True)
    body_type_detail = CarBodyTypeSerializer(source="body_type", read_only=True)
    fuel_detail = CarFuelTypeSerializer(source="fuel", read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            "url",
            "id", 
            "brand",
            "brand_detail",
            "model",
            "model_detail",
            "makeyear",
            "price",
            "body_type",
            "body_type_detail",
            "mileage",
            "condition",
            "condition_detail",
            "power",
            "fuel",
            "fuel_detail",
            "transmission",
            "transmission_detail",
            "is_online",
            ]
    
    def get_url(self,obj):
        req = self.context.get("request")
        if req is None:
            return None
        return reverse("listing-detail",kwargs={"pk": obj.pk},request=req)