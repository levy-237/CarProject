from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from config.mixins import VehicleDataPermission
from rest_framework import filters
from .models import Image, Listing
from .serializers import ListingImageCreateSerializer, ListingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ListingFilter

class ListingCreateAndList(
    # VehicleDataPermission,
                           generics.ListCreateAPIView):
    queryset = Listing.objects.filter(is_online=True)
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = ListingFilter
    ordering_fields = ['price', 'makeyear',"mileage"]
    ordering = ["id"]

    
    
class ListingDetailAndUpdate(
    # VehicleDataPermission,
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class ListingImageCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ListingImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser]