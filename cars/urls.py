from django.urls import path

from .views import (
    CarBodyTypeDetail,
    CarBodyTypeListCreate,
    CarBrandDetail,
    CarBrandListCreate,
    CarConditionDetail,
    CarConditionListCreate,
    CarDriveTrainDetail,
    CarDriveTrainListCreate,
    CarModelDetail,
    CarModelListCreate,
    CarModelTrimDetail,
    CarModelTrimListCreate,
)

urlpatterns = [
    path("body-types/", CarBodyTypeListCreate.as_view(), name="carbodytype-list"),
    path("body-types/<int:pk>/", CarBodyTypeDetail.as_view(), name="carbodytype-detail"),
    path("brands/", CarBrandListCreate.as_view(), name="carbrand-list"),
    path("brands/<int:pk>/", CarBrandDetail.as_view(), name="carbrand-detail"),
    path("models/", CarModelListCreate.as_view(), name="carmodel-list"),
    path("models/<int:pk>/", CarModelDetail.as_view(), name="carmodel-detail"),
    path("trims/", CarModelTrimListCreate.as_view(), name="carmodeltrim-list"),
    path("trims/<int:pk>/", CarModelTrimDetail.as_view(), name="carmodeltrim-detail"),
    path("drive-trains/", CarDriveTrainListCreate.as_view(), name="cardrivetrain-list"),
    path("drive-trains/<int:pk>/", CarDriveTrainDetail.as_view(), name="cardrivetrain-detail"),
    path("conditions/", CarConditionListCreate.as_view(), name="carcondition-list"),
    path("conditions/<int:pk>/", CarConditionDetail.as_view(), name="carcondition-detail"),
]
