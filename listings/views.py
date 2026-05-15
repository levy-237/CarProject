import os

import certifi
from django.conf import settings
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from config.mixins import ListingPermission, StaffPermission
from rest_framework import filters
from .models import Image, Listing
from .serializers import ListingImageCreateSerializer, ListingSerializer, ListingControlSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ListingFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import PriceHistory
from .uploadcare import get_uploadcare_client,create_uploadcare_image,destroy_uploadcare_image
from common.mail_services import send_email


class ListingCreateAndList(
    # ListingPermission,
    generics.ListCreateAPIView):
    queryset = Listing.objects.online()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = ListingFilter
    ordering_fields = ['price', 'makeyear',"mileage","publish_date"]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # change to admin
        send_email(to_name="Support", to_email="levanilominashvili23@gmail.com", subject="New Listing Created", text="A new listing has been created.")

    


class ListingDetailUpdateDelete(
    # ListingPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.online()
    serializer_class = ListingSerializer
    
    def perform_update(self, serializer):
        listing = serializer.instance
        if listing.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this listing.")
        new_price = serializer.validated_data.get("price")
        if new_price is not None and new_price != listing.price:
            PriceHistory.objects.create(listing=listing, old_price=listing.price)
        
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this listing.")
        for uuid in instance.images.exclude(uploadcare_uuid=""):
            destroy_uploadcare_image(uuid.uploadcare_uuid)

        instance.delete()
        
class ListingControlListCreateView(
    # StaffPermission,
    generics.ListAPIView):
    queryset = Listing.objects.offline()
    serializer_class = ListingControlSerializer
    
class ListingControlDetailView(
    # StaffPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.offline()
    serializer_class = ListingControlSerializer

    def perform_update(self, serializer):
        listing = serializer.instance
        owner = listing.owner
        

        serializer.save()
        if serializer.validated_data.get("is_online"):       
            # to the user  
            send_email(to_name=owner.username, to_email=owner.email, subject="Listing Online", text="A listing has been taken online.")

class FavouriteListingUpdate(
    ListingPermission,
    generics.CreateAPIView):
    serializer_class = ListingSerializer
    
    def create(self, request, *args, **kwargs):
        listing_id = self.kwargs['pk']
        listing = Listing.objects.get(id=listing_id)
        
        if request.user.favourite_listings.filter(id=listing_id).exists():
            request.user.favourite_listings.remove(listing)
            return Response({"data":"Successfully removed from favourites"}, status=status.HTTP_200_OK)
        
        request.user.favourite_listings.add(listing)
        return Response({"data": "Added to favourites."}, status=status.HTTP_201_CREATED)

                
                
class FavouriteListView(
    ListingPermission,
    generics.ListAPIView):
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        return self.request.user.favourite_listings.all()
    

class CompareListings(generics.ListAPIView):
    serializer_class = ListingSerializer
    def get_queryset(self):
        queryset = Listing.objects.online()
        ids = self.request.query_params.get("id")
        
        if not ids:
            raise ValidationError({"error":"id needs to be present"})
        
        listing_ids = [item.strip() for item in ids.split(",") if item.strip()]
        
        if len(listing_ids) > 3:
            raise ValidationError({"error":"maximum of 3 listings can be compared"})
        
        
        return queryset.filter(id__in=listing_ids)
        
        
class RecommendedListings(generics.ListAPIView):
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        queryset = Listing.objects.online()
        ids = self.request.query_params.get("id")
        
        if not ids:
            raise ValidationError({"error":"id needs to be present"})
        
        listing_ids = [item.strip() for item in ids.split(",") if item.strip()]
        selected_listings = Listing.objects.filter(id__in=listing_ids)

        if not selected_listings.exists():
            return queryset.none()

        rec_power = list(selected_listings.values_list("power", flat=True))
        rec_body = selected_listings.values_list("body_type", flat=True).distinct()

        min_power = min(rec_power)

        queryset = queryset.exclude(id__in=listing_ids)
        queryset = queryset.filter(power__gte=min_power)

        if rec_body:
            queryset = queryset.filter(body_type__in=rec_body)

        return queryset



class ListingByOwnerList(
    ListingPermission,
    generics.ListAPIView):  
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        return Listing.objects.by_owner(user=self.request.user)
    

class ListingImageCreateView(
    # ListingPermission,
    generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ListingImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        listing = serializer.validated_data.get("listing")
        image_file = serializer.validated_data.get("image")
        # if listing.owner != self.request.user:
        #     raise PermissionDenied("You are not the owner of this listing.")
        
        if image_file:
           uploadcare_file = create_uploadcare_image(image_file)
        
        serializer.save(
            image=uploadcare_file.cdn_url,
            uploadcare_uuid=uploadcare_file.uuid,
        )


class ListingImageDestroyView(
    # ListingPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ListingImageCreateSerializer

    def perform_destroy(self, instance):
        # if instance.listing.owner != self.request.user and not self.request.user.is_staff:
        #     raise PermissionDenied("You are not the owner of this image.")

        if instance.uploadcare_uuid:
            destroy_uploadcare_image(instance.uploadcare_uuid)
        instance.delete()

