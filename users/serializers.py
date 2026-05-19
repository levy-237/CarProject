from rest_framework import serializers
from .models import User, savedSearch, City, Province, ZipCode


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
        fields =["id","name","province","province_detail","zipcodes"]

class ZipcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields =["id","created_at","code","cities"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    picture_file = serializers.FileField(write_only=True, required=False)
    province_detail = ProvinceSimpleSerializer(source="province",read_only=True)
    city_detail = CitySimpleSerializer(source="city",read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username',"first_name","last_name", 'email', 'phone', 'password',"picture_file","picture", "uploadcare_uuid", "favourite_listings","saved_search","province","city","streetname_number","province_detail","city_detail"]
        read_only_fields = ["picture", "uploadcare_uuid", "favourite_listings","saved_search","province_detail","city_detail"]        
        
        
    def validate(self, data):
        province = data.get("province", getattr(self.instance, "province", None))
        city = data.get("city", getattr(self.instance, "city", None))
        
        if province and city and city.province_id != province.id:
            raise serializers.ValidationError(
                {"location": "Selected city does not belong to the selected province."}
            )
        return data
        
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def create(self, validated_data):
        favourite_listings = validated_data.pop("favourite_listings",[])
        picture_file = validated_data.pop("picture_file",None)
        
        user = User.objects.create_user(**validated_data)
        return user
    
    
class SavedSeachSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = savedSearch
        fields = ["id","created_at","owner","name","saved_url"]
        read_only_fields = ["owner"]
        