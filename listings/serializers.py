from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Image, Listing
from users.models import User
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


def validate_IntValue(value):
    if value is not None and value <= 0:
        raise serializers.ValidationError(
            {"value": "value can not be less than 1."}
        )


class ListingOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]

class ListingSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    owner = ListingOwnerSerializer(read_only=True)
    brand_detail = CarBrandSimpleSerializer(source="brand", read_only=True)
    model_detail = CarModelSimpleSerializer(source="model", read_only=True)
    condition_detail = CarConditionSerializer(source="condition", read_only=True)
    transmission_detail = CarTransmissionTypeSerializer(source="transmission", read_only=True)
    body_type_detail = CarBodyTypeSerializer(source="body_type", read_only=True)
    fuel_detail = CarFuelTypeSerializer(source="fuel", read_only=True)
    images = ListingImageSerializer(many=True,read_only=True)
    price = serializers.IntegerField(min_value=0)
    mileage = serializers.IntegerField(validators=[validate_IntValue])
    power = serializers.IntegerField(validators=[validate_IntValue])
    
    # online = serializers.BooleanField(source="is_online",read_only=True)
    # premium = serializers.BooleanField(source="is_premium",read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            "id",
            "url",
            "publish_date",
            "owner",
            "id", 
            "brand",
            "brand_detail",
            "model",
            "model_detail",
            "makeyear",
            "price",
            "old_price",
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
            "hidden",
            "images",
            ]
    
    

    def validate(self, data):
        brand = data.get("brand", getattr(self.instance, "brand", None))
        model = data.get("model", getattr(self.instance, "model", None))
 
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