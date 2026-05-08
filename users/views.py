from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from config.mixins import UserPermission
from rest_framework.exceptions import ValidationError
from listings.uploadcare import get_uploadcare_client,create_uploadcare_image,destroy_uploadcare_image

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self,serializer):
        image_file = serializer.validated_data.get("picture_file")
        
        
        uploadcare_file = create_uploadcare_image(image_file)

        serializer.save(
            picture=uploadcare_file.cdn_url,
            uploadcare_uuid=uploadcare_file.uuid
        )
        
           
class UserDetailView(
    # UserPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    
    serializer_class = UserSerializer


class UserMeView(
     # UserPermission,
    generics.RetrieveAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class UserListView(
    # UserPermission,
    generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

