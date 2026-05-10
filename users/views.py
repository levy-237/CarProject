from rest_framework import generics
from .models import User, savedSearch
from .serializers import UserSerializer, SavedSeachSerializer
from config.mixins import UserPermission
from rest_framework.exceptions import ValidationError, PermissionDenied
from listings.uploadcare import get_uploadcare_client,create_uploadcare_image,destroy_uploadcare_image


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self,serializer):
        image_file = serializer.validated_data.get("picture_file")
        
        if not image_file:
            serializer.save()
        
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
    
    def perform_destroy(self,instance):
        if instance.uploadcare_uuid:
            destroy_uploadcare_image(instance.uploadcare_uuid)
        
        instance.delete()
            


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



class AddSavedSearch(
    # UserPermission,
    generics.ListCreateAPIView
):
    queryset = savedSearch.objects.all()
    serializer_class = SavedSeachSerializer
    
    
    def perform_create(self,serializer):
        creator = self.request.user
        
        serializer.save(owner=creator)
        
    

class SavedSearchDetailUpdateDelete(
    # UserPermission,
    generics.RetrieveUpdateDestroyAPIView):
    
    queryset = savedSearch.objects.all()
    serializer_class = SavedSeachSerializer
    
    def perform_update(self,serializer):
        savedSearch = serializer.intance
        
        if savedSearch.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("you are not owner of this saved search")
        
        serializer.save()
            
        
    def perform_destroy(self,serializer):
        savedSearch = serializer.intance
        
        if savedSearch.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("you are not owner of this saved search")
        
        serializer.delete()
            
        
    
    