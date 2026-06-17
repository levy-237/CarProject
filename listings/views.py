from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from config.mixins import ListingPermission, StaffPermission, UserPermission
from rest_framework import filters
from .models import Image, Listing, PriceHistory, ListingReport
from django.db.models import F
from .serializers import ListingImageCreateSerializer, ListingSerializer,ListingListDetailSerializer, ListingControlSerializer,ListingManagementSerializer,ListingReportSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ListingFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .imagekit import create_image, destroy_image
from common.mail_services import send_email
from .saved_search import listing_matches_any_saved_search

class ListingCreateAndList(
    ListingPermission,
    generics.ListCreateAPIView):
    queryset = Listing.objects.online()
    serializer_class = ListingListDetailSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = ListingFilter
    ordering_fields = ['price', 'makeyear',"mileage","publish_date"]
    
    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_verified:
            raise PermissionDenied("For uploading listings, you need to verify your account")
        
        serializer.save(owner=user)
        # change to admin
        send_email(to_name="Support", to_email="levanilominashvili23@gmail.com", subject="New Listing Created", text="A new listing has been created.")

    


class ListingDetailUpdateDelete(
    ListingPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.online()
    serializer_class = ListingSerializer
    
    
    def get_object(self):
        listing = super().get_object()
        if self.request.method == "GET":
            listing.view_count = F("view_count") + 1
            listing.save(update_fields=["view_count"])
            listing.refresh_from_db()
            
        return listing
        
    
    def perform_update(self, serializer):
        user = self.request.user
        listing = serializer.instance
        if listing.owner != user and not user.is_staff:
            raise PermissionDenied("You are not the owner of this listing.")
        new_price = serializer.validated_data.get("price")
        if new_price is not None and new_price != listing.price:
            PriceHistory.objects.create(listing=listing, old_price=listing.price)
        
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(is_online=False, is_under_review=True)
    
    def perform_destroy(self, instance):
        user = self.request.user
        if instance.owner != user and not user.is_staff:
            raise PermissionDenied("You are not the owner of this listing.")
        for image in instance.images.exclude(storage_key=""):
            destroy_image(image.storage_key)

        instance.delete()
        
        
# control view for user submited listings that is under review
class ListingControlListView(
    StaffPermission,
    generics.ListAPIView):
    queryset = Listing.objects.is_under_review()
    serializer_class = ListingControlSerializer
    
class ListingControlDetailView(
    StaffPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.is_under_review()
    serializer_class = ListingControlSerializer

    def perform_update(self, serializer):
        listing = serializer.instance
        owner = listing.owner
        is_online = serializer.validated_data.get("is_online")
        is_under_review = serializer.validated_data.get("is_under_review")
        
        

        serializer.save()
        if is_online:
            users_with_alerts = listing_matches_any_saved_search(listing)
            # to the owner  
            send_email(to_name=owner.username, to_email=owner.email, subject="Listing Online", text="A listing has been taken online.")
            # checking saved searches
            if(users_with_alerts and len(users_with_alerts) > 0):
                for saved_search in users_with_alerts:
                    send_email(to_name=saved_search.owner.username, to_email=saved_search.owner.email, subject=f"new listing for saved search: {saved_search.name}", text=f"There is new listing online that matches your search agent! {saved_search.name}")
                    print(f"sucessfully sent mail to {saved_search.owner.email}")
                    


# management for listings any listings
class ListingManagementListView(
    StaffPermission,
    generics.ListCreateAPIView):
    queryset = Listing.objects.everything()
    serializer_class = ListingManagementSerializer


class ListingManagementDetailUpdateDelete(
    StaffPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.everything()
    serializer_class = ListingManagementSerializer




 
class FavouriteListingUpdate(
    ListingPermission,
    generics.CreateAPIView):
    serializer_class = ListingSerializer
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_verified:
            raise PermissionDenied("You need to be verified to favourite listings")
        listing_id = self.kwargs['pk']
        listing = Listing.objects.get(id=listing_id)
        
        if listing.owner == user:
            raise PermissionDenied("You cannot favourite your own listing")
            
        
        if user.favourite_listings.filter(id=listing_id).exists():
            user.favourite_listings.remove(listing)
            return Response({"data":"Successfully removed from favourites"}, status=status.HTTP_200_OK)
        
        user.favourite_listings.add(listing)
        return Response({"data": "Added to favourites."}, status=status.HTTP_201_CREATED)

                
                
class FavouriteListView(
    UserPermission,
    generics.ListAPIView):
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        return self.request.user.favourite_listings.all()
    

class CompareListings(generics.ListAPIView):
    serializer_class = ListingSerializer
    def get_queryset(self):
        queryset = Listing.objects.online()
        ids = self.request.query_params.get("ids")
        
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
    UserPermission,
    generics.ListAPIView):  
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        return Listing.objects.by_owner(user=self.request.user)
    

class ListingReportCreateView(
    # ListingPermission,
    generics.CreateAPIView):
    serializer_class = ListingReportSerializer
    queryset = ListingReport.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        listing = serializer.validated_data.get("listing")
        previous_reports = ListingReport.objects.filter(listing=listing).count()
        reporter = user if user.is_authenticated else None
        
        if  previous_reports >= 9:
            send_email(to_name="Support", to_email="levanilominashvili23@gmail.com", subject="Listing Reported", text=f"A listing has been reported {previous_reports} times.")
        
        serializer.save(reported_by=reporter, listing=listing)

class ListingReportList(
    StaffPermission,
    generics.ListAPIView):
    serializer_class = ListingReportSerializer
    queryset = ListingReport.objects.all().order_by("-created_at")

class ListingImageCreateView(
    UserPermission,
    generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ListingImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_verified:
            raise PermissionDenied("You need to be verified to create image")
        listing = serializer.validated_data.get("listing")
        image_file = serializer.validated_data.get("image")
        if listing.owner != user:
            raise PermissionDenied("You are not the owner of this listing.")
        
        if image_file:
           stored_image = create_image(image_file)
        
        serializer.save(
            image=stored_image.url,
            storage_key=stored_image.file_id,
        )
        
        if not self.request.user.is_staff:
           listing.is_online = False
           listing.is_under_review = True
           listing.save(update_fields=["is_online", "is_under_review"])

class ListingImageDestroyView(
    UserPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ListingImageCreateSerializer

    def perform_destroy(self, instance):
        if instance.listing.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this image.")

        if instance.storage_key:
            destroy_image(instance.storage_key)
        instance.delete()

