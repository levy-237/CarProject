from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from config.mixins import ListingPermission
from rest_framework import filters
from .models import Image, Listing,Province,City
from .serializers import ListingImageCreateSerializer, ListingSerializer,ProvinceSerializer,CitySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ListingFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import PriceHistory


class ListingCreateAndList(
    # ListingPermission,
    generics.ListCreateAPIView):
    queryset = Listing.objects.online()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = ListingFilter
    ordering_fields = ['price', 'makeyear',"mileage"]
    ordering = ["id"]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    


class ListingDetailUpdateDelete(
    # ListingPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.not_hidden()
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
        instance.delete()
        

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
        rec_trans = selected_listings.values_list("transmission", flat=True).distinct()
        rec_body = selected_listings.values_list("body_type", flat=True).distinct()
        rec_fuel = selected_listings.values_list("fuel", flat=True).distinct()

        min_power = min(rec_power)

        queryset = queryset.exclude(id__in=listing_ids)
        queryset = queryset.filter(power__gte=min_power)

        if rec_trans:
            queryset = queryset.filter(transmission__in=rec_trans)

        if rec_body:
            queryset = queryset.filter(body_type__in=rec_body)

        if rec_fuel:
            queryset = queryset.filter(fuel__in=rec_fuel)

        return queryset



class ListingByOwnerList(
    ListingPermission,
    generics.ListAPIView):  
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        return Listing.objects.by_owner(user=self.request.user)
    

class ListingImageCreateView(
    ListingPermission,
    generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ListingImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    
    
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
    