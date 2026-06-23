from rest_framework import generics
from common.query_helpers import filter_by_relation
from .models import User, savedSearch, Province, City,ZipCode
from .serializers import UserSerializer, SavedSeachSerializer, ProvinceSerializer, CitySerializer, ZipcodeSerializer
from config.mixins import UserPermission
from rest_framework.exceptions import ValidationError, PermissionDenied
from listings.imagekit import create_image, destroy_image
from common.mail_services import send_email
from urllib.parse import parse_qs
from .verification_code_generator import generate_verification_code
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from common.verification_code_helpers import hash_code, verify_code

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        image_file = serializer.validated_data.pop("picture_file", None)
        name = serializer.validated_data.get("first_name") + " " + serializer.validated_data.get("last_name")
        email = serializer.validated_data.get("email")
        
        if image_file:
            stored_image = create_image(image_file)
            serializer.save(
                picture=stored_image.url,
                storage_key=stored_image.file_id
            )
        else:
            serializer.save()
        
        send_email(name, email, "Levanchiko says Hi!!!, Thanks for signing up on our beatiful website", "Thanks for signing up on our beatiful website!, i hope you enjoy in!")
        
        
           
class UserDetailView(
    # UserPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_update(self, serializer):
        user = serializer.instance
        if user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only edit your own profile")
        
        serializer.save()
    
    def perform_destroy(self,instance):
        if self.request.user != instance and not self.request.user.is_staff: 
            raise PermissionDenied("You can only delete your own profile!")
        
        if instance.storage_key:
            destroy_image(instance.storage_key)
        
        instance.delete()
            


class SendEmailVerficationCode(
     UserPermission,
    APIView):

    
    def post(self,request):
        user = request.user

            
        if user.is_verified:
            return Response({"error":"You are already verified"}, status=400)
        
        
        verification_code = generate_verification_code()
        user.email_verification_code = hash_code(verification_code)
        user.email_verification_code_date = timezone.now()
        user.save(update_fields=["email_verification_code","email_verification_code_date"])  

        full_name =f"{user.first_name} {user.last_name}"
        
        send_email(full_name,user.email,"Verificaition code", f"Your verification code is here: {verification_code}")
        
        return Response({"message":"Verification code has been sent to email"})

        
        
class VerifyUser(
         UserPermission,
         APIView):
    
    def post(self,request):
        user = request.user
        

            
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
                
        if not verify_code(code, user.email_verification_code):
            return Response({"error":"Wrong verification code!"}, status=400)
        
        user.is_verified = True
        user.email_verification_code = None
        user.email_verification_code_date = None
        
        user.save(update_fields=["is_verified","email_verification_code","email_verification_code_date"])
        
        return Response({"message":"Succeefully verified User!"})
    

class SendPasswordRecoveryEmail(
    APIView):
    def post(self,request):
        email = request.data.get("email")
        
        if not email:
            return Response({"error":"Email is required!"}, status=400)
        

        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({"error":"No email with this address was found"}, status=404)
        
        time_now = timezone.now()
        verification_code = generate_verification_code()
        
        user.password_recovery_code = hash_code(verification_code)
        user.password_recovery_code_date = time_now
        
        user.save(update_fields=["password_recovery_code","password_recovery_code_date"])
        
        full_name =f"{user.first_name} {user.last_name}"
        
        send_email(full_name,user.email,"Password recovery code", f"Your Password recovery code is here: {verification_code}")
        
        return Response({"message":"Password recovery code has been sent to email"})

class RecoverPassword(
    APIView):
    def post(self,request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        code = self.request.data.get("code")
        
        if not email or not new_password or not code:
            return Response({"error":"Email, new password and recovery code are required!"}, status=400)
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({"error":"User not found"}, status=404)
        
        if not user.password_recovery_code or not user.password_recovery_code_date:
            return Response({"error":"You did not ask for recovery code"}, status=400)
        
        if user.check_password(new_password):
            return Response({"error":"This password has already been used in past"}, status=400)
            
        
        if not code:
            return Response({"error":"recovery code is required!"}, status=400)
            
        time_now = timezone.now()
        time_difference = time_now - user.password_recovery_code_date
        
        if time_difference.total_seconds() > 600:
            return Response({"error":"Recovery code expired!"}, status=400)
        
        if not verify_code(code, user.password_recovery_code):
            return Response({"error":"wrong recovery code"}, status=400)

        
        user.password_recovery_code = None
        user.password_recovery_code_date = None
        user.set_password(new_password)
        
        user.save(update_fields=["password_recovery_code","password_recovery_code_date","password"])
        
        return Response({"message":"Succeefully Recovevered your password!"})
        
        
class ChangePassword(
    UserPermission,
    APIView):
    
    def post(self,request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        
        user = request.user
        
        if not current_password or not new_password:
            return Response({"error":"Both fields need to be provided!"}, status=400)
        
        if not user.check_password(current_password):
            return Response({"error":"password is wrong!"},status=400)
        
        if current_password == new_password:
            return Response({"error":"This password has already been used in past"}, status=400)
            
        
        user.set_password(new_password)
        
        user.save(update_fields=["password"])
        
        return Response({"message":"Your password has been successfully changed!"})
        
        
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

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_by_relation(queryset, self.request, "province_id")
    
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
    