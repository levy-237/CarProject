from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from config.mixins import ListingPermission, DetailListingPermission
from rest_framework import filters
from .models import Image, Listing
from .serializers import ListingImageCreateSerializer, ListingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ListingFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

class ListingCreateAndList(
    ListingPermission,
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
    # DetailListingPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.not_hidden()
    serializer_class = ListingSerializer
    
    def perform_update(self, serializer):
        listing = serializer.instance
        if listing.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this listing.")
        new_price = serializer.validated_data.get("price")
        if new_price is None or new_price == listing.price:
            serializer.save()
            return
        serializer.save(old_price=listing.price)
    
    def perform_destroy(self, instance):
        if instance.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You are not the owner of this listing.")
        instance.delete()
        

class FavouriteListingUpdate(
    # ListingPermission,
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
    # ListingPermission,
    generics.ListAPIView):
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        return self.request.user.favourite_listings.all()


class ListingByOwnerList(
    # ListingPermission,
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