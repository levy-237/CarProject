from rest_framework import serializers

from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="car.brand.brand", read_only=True)
    model_name = serializers.CharField(source="car.model.model", read_only=True)
    car_id = serializers.IntegerField(source="car.id", read_only=True)
    
    class Meta:
        model = Listing
        fields = ["id", "publish_date","car", "car_id", "brand_name", "model_name"]