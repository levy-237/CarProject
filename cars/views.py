from rest_framework import generics
from config.mixins import VehicleDataPermission
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


class CarBodyTypeListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarBodyType.objects.all()
    serializer_class = CarBodyTypeSerializer


class CarBodyTypeDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBodyType.objects.all()
    serializer_class = CarBodyTypeSerializer


class CarBrandListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarBrandDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarModelListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarModelDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarConditionListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarCondition.objects.all()
    serializer_class = CarConditionSerializer


class CarConditionDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarCondition.objects.all()
    serializer_class = CarConditionSerializer


class CarFuelTypeListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarFuelType.objects.all()
    serializer_class = CarFuelTypeSerializer


class CarFuelTypeDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarFuelType.objects.all()
    serializer_class = CarFuelTypeSerializer


class CarTransmissionTypeListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarTransmissionType.objects.all()
    serializer_class = CarTransmissionTypeSerializer


class CarTransmissionTypeDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarTransmissionType.objects.all()
    serializer_class = CarTransmissionTypeSerializer


