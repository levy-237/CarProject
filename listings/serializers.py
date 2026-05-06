from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Image, Listing,Province,City
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

class CitySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]
     
class ProvinceSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name"]
        

class ProvinceSerializer(serializers.ModelSerializer):
    connected_cities_detail = CitySimpleSerializer(source="connected_cities",read_only=True,many=True)

    class Meta:
        model = Province
        fields = ["id","name","connected_cities","connected_cities_detail"]


class CitySerializer(serializers.ModelSerializer):
    province_detail = ProvinceSimpleSerializer(source="province",read_only=True)
    class Meta:
        model = City
        fields =["id","name","province","province_detail"]



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
    province_detail = ProvinceSimpleSerializer(source="province",read_only=True)
    city_detail = CitySimpleSerializer(source="city",read_only=True)
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
            "title", 
            "brand",
            "brand_detail",
            "model",
            "model_detail",
            "makeyear",
            "price",
            "price_history",
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
            "description",
            "province",
            "province_detail",
            "city",
            "city_detail",
            "is_online",
            "is_premium",
            "hidden",
            "images",
            ]
    
    

    def validate(self, data):
        brand = data.get("brand", getattr(self.instance, "brand", None))
        model = data.get("model", getattr(self.instance, "model", None))
        province = data.get("province", getattr(self.instance, "province", None))
        city = data.get("city", getattr(self.instance, "city", None))
        
 
        if brand and model and model.connected_brand_id != brand.id:
            raise serializers.ValidationError(
                {"model": "Selected model does not belong to the selected brand."}
            )
        if province and city and city.province_id != province.id:
            raise serializers.ValidationError(
                {"location": "Selected city does not belong to the selected province."}
            )

        return data
    
    def get_url(self,obj):
        req = self.context.get("request")
        if req is None:
            return None
        return reverse("listing-detail",kwargs={"pk": obj.pk},request=req)