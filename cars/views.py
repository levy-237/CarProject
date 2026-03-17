from rest_framework import generics

from .models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarFuelType,
    CarModel,
    CarTransmissionType,
)
from .serializers import (
    CarBodyTypeSerializer,
    CarBrandSerializer,
    CarConditionSerializer,
    CarFuelTypeSerializer,
    CarModelSerializer,
    CarTransmissionTypeSerializer,
)


class CarBodyTypeListCreate(generics.ListCreateAPIView):
    queryset = CarBodyType.objects.all()
    serializer_class = CarBodyTypeSerializer


class CarBodyTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBodyType.objects.all()
    serializer_class = CarBodyTypeSerializer


class CarBrandListCreate(generics.ListCreateAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarBrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarModelListCreate(generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarConditionListCreate(generics.ListCreateAPIView):
    queryset = CarCondition.objects.all()
    serializer_class = CarConditionSerializer


class CarConditionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarCondition.objects.all()
    serializer_class = CarConditionSerializer


class CarFuelTypeListCreate(generics.ListCreateAPIView):
    queryset = CarFuelType.objects.all()
    serializer_class = CarFuelTypeSerializer


class CarFuelTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarFuelType.objects.all()
    serializer_class = CarFuelTypeSerializer


class CarTransmissionTypeListCreate(generics.ListCreateAPIView):
    queryset = CarTransmissionType.objects.all()
    serializer_class = CarTransmissionTypeSerializer


class CarTransmissionTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarTransmissionType.objects.all()
    serializer_class = CarTransmissionTypeSerializer


