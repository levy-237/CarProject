from rest_framework import generics
from config.mixins import VehicleDataPermission
from .models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarDriveTrain,
    CarModel,
    CarModelTrim,
)
from .serializers import (
    CarBodyTypeSerializer,
    CarBrandSerializer,
    CarConditionSerializer,
    CarDriveTrainSerializer,
    CarModelSerializer,
    CarModelTrimSerializer,
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


class CarModelTrimListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarModelTrim.objects.all()
    serializer_class = CarModelTrimSerializer



class CarModelTrimDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModelTrim.objects.all()
    serializer_class = CarModelTrimSerializer


class CarDriveTrainListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarDriveTrain.objects.all()
    serializer_class = CarDriveTrainSerializer


class CarDriveTrainDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarDriveTrain.objects.all()
    serializer_class = CarDriveTrainSerializer


class CarConditionListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarCondition.objects.all()
    serializer_class = CarConditionSerializer


class CarConditionDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarCondition.objects.all()
    serializer_class = CarConditionSerializer


