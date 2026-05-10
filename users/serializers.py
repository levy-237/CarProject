from rest_framework import serializers
from .models import User, savedSearch

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    picture_file = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username',"first_name","last_name", 'email', 'phone', 'password',"picture_file","picture", "uploadcare_uuid", "favourite_listings","saved_search"]
        read_only_fields = ["picture", "uploadcare_uuid", "favourite_listings"]        
        
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
        