from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Image, Listing, PriceHistory
from users.models import User
from cars.serializers import CarBrandSimpleSerializer,CarModelSimpleSerializer,CarConditionSerializer,CarTransmissionTypeSerializer,CarBodyTypeSerializer,CarFuelTypeSerializer


class ListingImageSerializer(serializers.ModelSerializer):
    local_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Image
        fields = ["id","local_url", "image", "uploadcare_uuid", "created_at"]
    
    def get_local_url(self,obj):
        req = self.context.get("request")
        if req is None:
            return None
        return reverse("listing-image-detail",kwargs={"pk": obj.pk},request=req)


class ListingImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    
    class Meta:
        model = Image
        fields = ["id", "listing", "image", "uploadcare_uuid", "created_at"]
        read_only_fields = ["id", "uploadcare_uuid", "created_at"]

    def to_representation(self, instance):
        return ListingImageSerializer(instance, context=self.context).data



def validate_IntValue(value):
    if value is not None and value <= 0:
        raise serializers.ValidationError(
            {"value": "value can not be less than 1."}
        )


class ListingOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields =["listing","old_price","created_at"]

class ListingSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    owner = ListingOwnerSerializer(read_only=True)
    brand_detail = CarBrandSimpleSerializer(source="brand", read_only=True)
    model_detail = CarModelSimpleSerializer(source="model", read_only=True)
    condition_detail = CarConditionSerializer(source="condition", read_only=True)
    transmission_detail = CarTransmissionTypeSerializer(source="transmission", read_only=True)
    body_type_detail = CarBodyTypeSerializer(source="body_type", read_only=True)
    fuel_detail = CarFuelTypeSerializer(source="fuel", read_only=True)
    price_history = PriceHistorySerializer(many=True)
    images = ListingImageSerializer(many=True,read_only=True)

    price = serializers.IntegerField(min_value=0)
    mileage = serializers.IntegerField(validators=[validate_IntValue])
    power = serializers.IntegerField(validators=[validate_IntValue])
    is_favourite = serializers.SerializerMethodField(read_only=True)
    
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
            "is_favourite",
            "is_online",
            "is_premium",
            "is_sold",
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
    
    def get_is_favourite(self,obj):
        req = self.context.get("request")
        
        if not req.user.is_authenticated: 
            return False
        
        return req.user.favourite_listings.filter(id=obj.id).exists()

        
    def create(self,validated_data):
        price_history = validated_data.pop("price_history",None)
        
        listing = Listing.objects.create(**validated_data)
        return listing