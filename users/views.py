from rest_framework import generics
from .models import User, savedSearch, Province, City,ZipCode
from .serializers import UserSerializer, SavedSeachSerializer, ProvinceSerializer, CitySerializer, ZipcodeSerializer
from config.mixins import UserPermission
from rest_framework.exceptions import ValidationError, PermissionDenied
from listings.imagekit import create_image, destroy_image
from common.mail_services import send_email
from urllib.parse import parse_qs
from random import randint
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self,serializer):
        image_file = serializer.validated_data.pop("picture_file", None)
        name = serializer.validated_data.get("first_name") + " " + serializer.validated_data.get("last_name")
        email = serializer.validated_data.get("email")
        
        if not image_file:
           return serializer.save()
        
        stored_image = create_image(image_file)
        serializer.save(
            picture=stored_image.url,
            storage_key=stored_image.file_id
        )
        # to user
        send_email(name, email, "Levanchiko says Hi!!!, Thanks for signing up on our beatiful website", "Thanks for signing up on our beatiful website!, i hope you enjoy in!")
        
        
           
class UserDetailView(
    # UserPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_destroy(self,instance):
        if instance.storage_key:
            destroy_image(instance.storage_key)
        
        instance.delete()
            


class SendEmailVerficationCode(
     # UserPermission,
    APIView):

    
    def post(self,request):
        user = request.user

        if not user.is_authenticated:
            return Response({"error":"You are not logged in"}, status=400)
            
        if user.is_verified:
            return Response({"error":"You are already verified"}, status=400)
        
        
        verification_number = randint(100000, 999999)
        user.email_verification_code = verification_number
        user.email_verification_code_date = timezone.now()
        user.save(update_fields=["email_verification_code","email_verification_code_date"])  

        full_name =f"{user.first_name} {user.last_name}"
        
        send_email(full_name,user.email,"Verificaition code", f"Your verification code is here: {verification_number}")
        
        return Response({"message":"Verification code has been sent to email"})

        
        
class VerifyUser(
         # UserPermission,
         APIView):
    
    def post(self,request):
        user = request.user
        
        if not user.is_authenticated:
            return Response({"error":"You are not logged in"}, status=400)
            
        if not user.email_verification_code_date or not user.email_verification_code:
            return Response({"error":"No verification request made!"},status=400)
                
        time_now = timezone.now()
        time_difference = time_now - user.email_verification_code_date
        code = self.request.data.get("code")
        
        if user.is_verified:
            return Response({"error":"You are already verified"}, status=400)
        

        if time_difference.total_seconds() > 600:
            return Response({"error":"Verification code expired!"}, status=400)
        
        if not code:
            return Response({"error":"Verification code is required!"}, status=400)
                
        if str(code) != str(user.email_verification_code):
            return Response({"error":"Wrong verification code!"}, status=400)
        
        user.is_verified = True
        user.email_verification_code = None
        user.email_verification_code_date = None
        
        user.save(update_fields=["is_verified","email_verification_code","email_verification_code_date"])
        
        return Response({"message":"Succeefully verified User!"})
   
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
    
    
    def get_object(self):
        obj = super().get_object()  
        params = parse_qs(obj.saved_url)
        print(params)

        return obj
    
    def perform_update(self,serializer):
        savedSearch = serializer.instance
        
        if savedSearch.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("you are not owner of this saved search")
        
        serializer.save()
            
        
    def perform_destroy(self, instance):
        if instance.owner != self.request.user and not self.request.user.is_staff:
           raise PermissionDenied("You are not owner of this saved search")

        instance.delete()
            
        
    
    

class ProvinceList(
    # ListingPermission,
    generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    
class ProvinceDetailUpdateDestroy(
    # ListingPermission,
      generics.RetrieveUpdateDestroyAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    
class CityList(
    # ListingPermission,
    generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
class CityDetailUpdateDestroy(
    # ListingPermission,
      generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class ZipCodeList(
    # ListingPermission,
    generics.ListCreateAPIView):
    queryset = ZipCode.objects.all()
    serializer_class = ZipcodeSerializer
    
class ZipCodeDetailUpdateDestroy(
    # ListingPermission,
      generics.RetrieveUpdateDestroyAPIView):
    queryset = ZipCode.objects.all()
    serializer_class = ZipcodeSerializer
    