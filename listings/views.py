from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from config.mixins import ListingPermission, DetailListingPermission
from rest_framework import filters
from .models import Image, Listing
from .serializers import ListingImageCreateSerializer, ListingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ListingFilter

class ListingCreateAndList(
    ListingPermission,
                           generics.ListCreateAPIView):
    queryset = Listing.objects.online()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = ListingFilter
    ordering_fields = ['price', 'makeyear',"mileage"]
    ordering = ["id"]

    

class ListingByOwnerList(
    ListingPermission,
    generics.ListAPIView):
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        return Listing.objects.by_owner(user=self.request.user)
    

class ListingDetailAndUpdate(
    # DetailListingPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.online()
    serializer_class = ListingSerializer


class ListingImageCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ListingImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser]