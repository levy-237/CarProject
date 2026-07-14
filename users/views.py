from rest_framework import generics
from common.query_helpers import filter_by_relation
from .models import User, savedSearch, Province, City,ZipCode
from .serializers import UserSerializer, SavedSeachSerializer, ProvinceSerializer, CitySerializer, ZipcodeSerializer
from config.mixins import UserPermission, VehicleDataPermission
from rest_framework.exceptions import ValidationError, PermissionDenied
from listings.imagekit import create_image, destroy_image
from common.mail_services import send_email_safely
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
        
        send_email_safely(name, email, "Levanchiko says Hi!!!, Thanks for signing up on our beatiful website", "Thanks for signing up on our beatiful website!, i hope you enjoy in!")
        
        
class UserCompanyListView(
    UserPermission,
    generics.ListAPIView
):
    queryset = User.objects.filter(is_private=False)
    serializer_class = UserSerializer

class UserDetailView(
    UserPermission,
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
            raise PermissionDenied("Du kannst nur dein eigenes Profil löschen.")
        
        if instance.storage_key:
            destroy_image(instance.storage_key)
        
        instance.delete()
            


class SendEmailVerficationCode(
     UserPermission,
    APIView):

    
    def post(self,request):
        user = request.user

            
        if user.is_verified:
            return Response({"detail":"Du bist bereits verifiziert."}, status=400)
        
        
        verification_code = generate_verification_code()
        user.email_verification_code = hash_code(verification_code)
        user.email_verification_code_date = timezone.now()
        user.save(update_fields=["email_verification_code","email_verification_code_date"])  

        full_name =f"{user.first_name} {user.last_name}"
        
        send_email_safely(full_name,user.email,"Verificaition code", f"Your verification code is here: {verification_code}")
        
        return Response({"message":"Der Verifizierungscode wurde per E-Mail gesendet."})

        
        
class VerifyUser(
         UserPermission,
         APIView):
    
    def post(self,request):
        user = request.user
        

            
        if not user.email_verification_code_date or not user.email_verification_code:
            return Response({"detail":"Es wurde keine Verifizierungsanfrage gestellt."},status=400)
                
        time_now = timezone.now()
        time_difference = time_now - user.email_verification_code_date
        code = self.request.data.get("code")
        
        if user.is_verified:
            return Response({"detail":"Du bist bereits verifiziert."}, status=400)
        

        if time_difference.total_seconds() > 600:
            return Response({"detail":"Der Verifizierungscode ist abgelaufen."}, status=400)
        
        if not code:
            return Response({"detail":"Der Verifizierungscode ist erforderlich."}, status=400)
                
        if not verify_code(code, user.email_verification_code):
            return Response({"detail":"Falscher Verifizierungscode."}, status=400)
        
        user.is_verified = True
        user.email_verification_code = None
        user.email_verification_code_date = None
        
        user.save(update_fields=["is_verified","email_verification_code","email_verification_code_date"])
        
        return Response({"message":"Benutzer wurde erfolgreich verifiziert."})
    

class SendPasswordRecoveryEmail(
    APIView):
    def post(self,request):
        email = request.data.get("email")
        
        if not email:
            return Response({"detail":"E-Mail ist erforderlich."}, status=400)
        

        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({"detail":"Es wurde kein Konto mit dieser E-Mail-Adresse gefunden."}, status=404)
        
        time_now = timezone.now()
        verification_code = generate_verification_code()
        
        user.password_recovery_code = hash_code(verification_code)
        user.password_recovery_code_date = time_now
        
        user.save(update_fields=["password_recovery_code","password_recovery_code_date"])
        
        full_name =f"{user.first_name} {user.last_name}"
        
        send_email_safely(
            full_name,
            user.email,
            "Password recovery code",
            f"Your password recovery for user {user.username} is here: {verification_code}",
        )
        
        return Response({"message":"Der Code zur Passwortwiederherstellung wurde per E-Mail gesendet."})

class RecoverPassword(
    APIView):
    def post(self,request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        code = self.request.data.get("code")
        
        if not email or not new_password or not code:
            return Response({"detail":"E-Mail, neues Passwort und Wiederherstellungscode sind erforderlich."}, status=400)
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response({"detail":"Benutzer wurde nicht gefunden."}, status=404)
        
        if not user.password_recovery_code or not user.password_recovery_code_date:
            return Response({"detail":"Es wurde kein Wiederherstellungscode angefordert."}, status=400)
        
        if user.check_password(new_password):
            return Response({"detail":"Dieses Passwort wurde bereits verwendet."}, status=400)
            
        
        if not code:
            return Response({"detail":"Der Wiederherstellungscode ist erforderlich."}, status=400)
            
        time_now = timezone.now()
        time_difference = time_now - user.password_recovery_code_date
        
        if time_difference.total_seconds() > 600:
            return Response({"detail":"Der Wiederherstellungscode ist abgelaufen."}, status=400)
        
        if not verify_code(code, user.password_recovery_code):
            return Response({"detail":"Falscher Wiederherstellungscode."}, status=400)

        
        user.password_recovery_code = None
        user.password_recovery_code_date = None
        user.set_password(new_password)
        
        user.save(update_fields=["password_recovery_code","password_recovery_code_date","password"])
        
        return Response({"message":"Dein Passwort wurde erfolgreich wiederhergestellt."})
        
        
class ChangePassword(
    UserPermission,
    APIView):
    
    def post(self,request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        
        user = request.user
        
        if not current_password or not new_password:
            return Response({"detail":"Beide Felder müssen angegeben werden."}, status=400)
        
        if not user.check_password(current_password):
            return Response({"detail":"Das Passwort ist falsch."},status=400)
        
        if current_password == new_password:
            return Response({"detail":"Dieses Passwort wurde bereits verwendet."}, status=400)
            
        
        user.set_password(new_password)
        
        user.save(update_fields=["password"])
        
        return Response({"message":"Dein Passwort wurde erfolgreich geändert."})
        
        
class UserMeView(
     UserPermission,
    generics.RetrieveAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class UserListView(
    UserPermission,
    generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class AddSavedSearch(
    UserPermission,
    generics.ListCreateAPIView
):
    queryset = savedSearch.objects.all()
    serializer_class = SavedSeachSerializer
    
    
    def perform_create(self,serializer):
        creator = self.request.user
        
        serializer.save(owner=creator)
        
    

class SavedSearchDetailUpdateDelete(
    UserPermission,
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
            raise PermissionDenied("Du bist nicht der Besitzer dieser gespeicherten Suche.")
        
        serializer.save()
            
        
    def perform_destroy(self, instance):
        if instance.owner != self.request.user and not self.request.user.is_staff:
           raise PermissionDenied("Du bist nicht der Besitzer dieser gespeicherten Suche.")

        instance.delete()
            
        
    
    

class ProvinceList(
    VehicleDataPermission,
    generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    
class ProvinceDetailUpdateDestroy(
    VehicleDataPermission,
      generics.RetrieveUpdateDestroyAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    
class CityList(
    VehicleDataPermission,
    generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_by_relation(queryset, self.request, "province_id")
    
class CityDetailUpdateDestroy(
    VehicleDataPermission,
      generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class ZipCodeList(
    VehicleDataPermission,
    generics.ListCreateAPIView):
    queryset = ZipCode.objects.all()
    serializer_class = ZipcodeSerializer
    
class ZipCodeDetailUpdateDestroy(
    VehicleDataPermission,
      generics.RetrieveUpdateDestroyAPIView):
    queryset = ZipCode.objects.all()
    serializer_class = ZipcodeSerializer
    