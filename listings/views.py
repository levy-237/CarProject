from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics
from datetime import date
from .models import Listing
from .serializers import ListingSerializer

class ListingCreateAndList(generics.ListCreateAPIView):
    serializer_class = ListingSerializer
    
    def get_queryset(self):
        qs = Listing.objects.all()
        brandId = (self.request.query_params.getlist('brand') or '')
        bodyTypeId = (self.request.query_params.getlist('body') or '')
        modelId = (self.request.query_params.getlist('model') or '')
        conditionId = (self.request.query_params.getlist('condition') or '')
        fuelTypeId = (
            self.request.query_params.getlist('fuel')
            or ''
        )
        transmissionTypeId = (
         self.request.query_params.getlist('transmission')
            or ''
        )
        minDate = self.request.query_params.get("mindate")
        maxDate = self.request.query_params.get("maxdate")
        minPrice = self.request.query_params.get("minprice")
        maxPrice = self.request.query_params.get("maxprice")
        minMileage = self.request.query_params.get("minmileage")
        maxMileage = self.request.query_params.get("maxmileage")
        
        minDateObject = None
        maxDateObject = None
        
        if minDate:
            intDate = int(minDate.strip())
            minDateObject = date(intDate,12,31)
        else:
            minDateObject = None
            
        if maxDate:
            intDate = int(maxDate.strip())
            maxDateObject = date(intDate,12,31)
        else:
            maxDateObject = None
            
        
        filters = Q(is_online=True)
        if minMileage:
            filters &= Q(mileage__gte=minMileage)
        if maxMileage:
            filters &= Q(mileage__lte=maxMileage)
        if minPrice:
            filters &= Q(price__gte=minPrice)
        if maxPrice:
            filters &= Q(price__lte=maxPrice)
        if minDateObject:
            filters &= Q(makeyear__gte=minDateObject)
        if maxDateObject:
            filters &= Q(makeyear__lte=maxDateObject)
        if bodyTypeId:
            filters &= Q(body_type_id__in=bodyTypeId)
        if brandId:
            filters &= Q(brand_id__in=brandId)
        if modelId:
            filters &= Q(model_id__in=modelId)
        if conditionId:
            filters &= Q(condition_id__in=conditionId)
        if fuelTypeId:
            filters &= Q(fuel_id__in=fuelTypeId)
        if transmissionTypeId:
            filters &= Q(transmission_id__in=transmissionTypeId)

        return qs.filter(filters)
    
class ListingDetailAndUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer