from django.urls import path

from .views import (
    CarBodyTypeDetail,
    CarBodyTypeListCreate,
    CarBrandDetail,
    CarBrandList,
    CarBrandListCreate,
    CarConditionDetail,
    CarConditionListCreate,
    CarDriveTrainDetail,
    CarDriveTrainListCreate,
    CarModelDetail,
    CarModelList,
    CarModelListCreate,
    CarModelTrimDetail,
    CarModelTrimList,
    CarModelTrimListCreate,
)

urlpatterns = [
    path("body-types/", CarBodyTypeListCreate.as_view(), name="carbodytype-list"),
    path("body-types/<int:pk>/", CarBodyTypeDetail.as_view(), name="carbodytype-detail"),
    path("brands/", CarBrandList.as_view(), name="carbrand-list"),
    path("models/", CarModelList.as_view(), name="carmodel-list"),
    path("trims/", CarModelTrimList.as_view(), name="carmodeltrim-list"),
    path("control-brands/", CarBrandListCreate.as_view(), name="carbrand-control-list"),
    path("control-brands/<int:pk>/", CarBrandDetail.as_view(), name="carbrand-control-detail"),
    path("control-models/", CarModelListCreate.as_view(), name="carmodel-control-list"),
    path("control-models/<int:pk>/", CarModelDetail.as_view(), name="carmodel-control-detail"),
    path("control-trims/", CarModelTrimListCreate.as_view(), name="carmodeltrim-control-list"),
    path("control-trims/<int:pk>/", CarModelTrimDetail.as_view(), name="carmodeltrim-control-detail"),
    path("drive-trains/", CarDriveTrainListCreate.as_view(), name="cardrivetrain-list"),
    path("drive-trains/<int:pk>/", CarDriveTrainDetail.as_view(), name="cardrivetrain-detail"),
    path("conditions/", CarConditionListCreate.as_view(), name="carcondition-list"),
    path("conditions/<int:pk>/", CarConditionDetail.as_view(), name="carcondition-detail"),
]
