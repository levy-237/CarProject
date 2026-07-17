from rest_framework import generics
from config.mixins import AdminOrReadOnlyPermissionMixin
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


class CarBodyTypeListCreate(AdminOrReadOnlyPermissionMixin, generics.ListCreateAPIView):
    queryset = CarBodyType.objects.all().order_by("name")
    serializer_class = CarBodyTypeSerializer



class CarBodyTypeDetail(AdminOrReadOnlyPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBodyType.objects.all()
    serializer_class = CarBodyTypeSerializer


class CarBrandList(generics.ListAPIView):
    queryset = CarBrand.objects.all().order_by("name")
    serializer_class = CarBrandSimpleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class CarBrandListCreate(AdminOrReadOnlyPermissionMixin, generics.ListCreateAPIView):
    queryset = CarBrand.objects.all().order_by("name")
    serializer_class = CarBrandSerializer

class CarBrandDetail(AdminOrReadOnlyPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer

class CarModelList(generics.ListAPIView):
    queryset = CarModel.objects.all().order_by("name")
    serializer_class = CarModelSimpleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = filter_by_relation(queryset, self.request, "connected_brand_id")
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class CarModelListCreate(AdminOrReadOnlyPermissionMixin, generics.ListCreateAPIView):
    queryset = CarModel.objects.all().order_by("name")
    serializer_class = CarModelSerializer

class CarModelDetail(AdminOrReadOnlyPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer

class CarModelTrimList(generics.ListAPIView):
    queryset = CarModelTrim.objects.all().order_by("name")
    serializer_class = CarModelTrimNameSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = filter_by_relation(queryset, self.request, "connected_model_id")
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class CarModelTrimListCreate(AdminOrReadOnlyPermissionMixin, generics.ListCreateAPIView):
    queryset = CarModelTrim.objects.all().order_by("name")
    serializer_class = CarModelTrimSerializer


class CarModelTrimDetail(AdminOrReadOnlyPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarModelTrim.objects.all()
    serializer_class = CarModelTrimSerializer

class CarDriveTrainListCreate(AdminOrReadOnlyPermissionMixin, generics.ListCreateAPIView):
    queryset = CarDriveTrain.objects.all().order_by("name")
    serializer_class = CarDriveTrainSerializer

class CarDriveTrainDetail(AdminOrReadOnlyPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarDriveTrain.objects.all()
    serializer_class = CarDriveTrainSerializer

class CarConditionListCreate(AdminOrReadOnlyPermissionMixin, generics.ListCreateAPIView):
    queryset = CarCondition.objects.all().order_by("name")
    serializer_class = CarConditionSerializer

class CarConditionDetail(AdminOrReadOnlyPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = CarCondition.objects.all()
    serializer_class = CarConditionSerializer

