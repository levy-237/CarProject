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
from common.query_helpers import filter_by_relation
from .serializers import (
    CarBodyTypeSerializer,
    CarBrandSerializer,
    CarBrandSimpleSerializer,
    CarConditionSerializer,
    CarDriveTrainSerializer,
    CarModelSerializer,
    CarModelSimpleSerializer,
    CarModelTrimNameSerializer,
    CarModelTrimSerializer,
)


class CarBodyTypeListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarBodyType.objects.all()
    serializer_class = CarBodyTypeSerializer


class CarBodyTypeDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBodyType.objects.all()
    serializer_class = CarBodyTypeSerializer


class CarBrandList(VehicleDataPermission, generics.ListAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSimpleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class CarBrandListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarBrandDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarModelList(VehicleDataPermission, generics.ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSimpleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = filter_by_relation(queryset, self.request, "connected_brand_id")
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class CarModelListCreate(VehicleDataPermission, generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarModelDetail(VehicleDataPermission, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class CarModelTrimList(VehicleDataPermission, generics.ListAPIView):
    queryset = CarModelTrim.objects.all()
    serializer_class = CarModelTrimNameSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = filter_by_relation(queryset, self.request, "connected_model_id")
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


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


