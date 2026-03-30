from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Image, Listing
from cars.serializers import CarBrandSimpleSerializer,CarModelSimpleSerializer,CarConditionSerializer,CarTransmissionTypeSerializer,CarBodyTypeSerializer,CarFuelTypeSerializer


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image", "created_at"]


class ListingImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "listing",  "image", "created_at"]
        read_only_fields = ["id", "created_at"]


class ListingSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    brand_detail = CarBrandSimpleSerializer(source="brand", read_only=True)
    model_detail = CarModelSimpleSerializer(source="model", read_only=True)
    condition_detail = CarConditionSerializer(source="condition", read_only=True)
    transmission_detail = CarTransmissionTypeSerializer(source="transmission", read_only=True)
    body_type_detail = CarBodyTypeSerializer(source="body_type", read_only=True)
    fuel_detail = CarFuelTypeSerializer(source="fuel", read_only=True)
    images = ListingImageSerializer(many=True,read_only=True)
    # online = serializers.BooleanField(source="is_online",read_only=True)
    # premium = serializers.BooleanField(source="is_premium",read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            "url",
            "publish_date",
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
            "is_premium",
            "images",
            ]

    def validate(self, data):
        brand = data.get("brand", getattr(self.instance, "brand", None))
        model = data.get("model", getattr(self.instance, "model", None))
        price = data.get("price", getattr(self.instance, "price", None))
        mileage = data.get("mileage", getattr(self.instance, "mileage", None))
        
        
        
        if price is not None and price <= 0:
            raise serializers.ValidationError(
                {"price": "price can not be less than 1."}
            )
        
        if mileage is not None and mileage <= 0:
            raise serializers.ValidationError(
                {"mileage": "mileage can not be less than 1."}
            )
        if brand and model and model.connected_brand_id != brand.id:
            raise serializers.ValidationError(
                {"model": "Selected model does not belong to the selected brand."}
            )

        return data
    
    def get_url(self,obj):
        req = self.context.get("request")
        if req is None:
            return None
        return reverse("listing-detail",kwargs={"pk": obj.pk},request=req)