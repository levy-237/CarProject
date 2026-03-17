from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            "url",
            "id", 
            "brand",
            "model",
            "makeyear",
            "price",
            "body_type",
            "mileage",
            "condition",
            "power",
            "fuel",
            "transmission",
            "is_online",
            ]
    
    def get_url(self,obj):
        req = self.context.get("request")
        if req is None:
            return None
        return reverse("listing-detail",kwargs={"pk": obj.pk},request=req)