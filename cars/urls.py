from django.urls import path

from .views import (
    CarBodyTypeDetail,
    CarBodyTypeListCreate,
    CarBrandDetail,
    CarBrandListCreate,
    CarConditionDetail,
    CarConditionListCreate,
    CarFuelTypeDetail,
    CarFuelTypeListCreate,
    CarModelDetail,
    CarModelListCreate,
    CarTransmissionTypeDetail,
    CarTransmissionTypeListCreate,
)

urlpatterns = [
    path("body-types/", CarBodyTypeListCreate.as_view(), name="carbodytype-list"),
    path("body-types/<int:pk>/", CarBodyTypeDetail.as_view(), name="carbodytype-detail"),
    path("brands/", CarBrandListCreate.as_view(), name="carbrand-list"),
    path("brands/<int:pk>/", CarBrandDetail.as_view(), name="carbrand-detail"),
    path("models/", CarModelListCreate.as_view(), name="carmodel-list"),
    path("models/<int:pk>/", CarModelDetail.as_view(), name="carmodel-detail"),
    path("conditions/", CarConditionListCreate.as_view(), name="carcondition-list"),
    path("conditions/<int:pk>/", CarConditionDetail.as_view(), name="carcondition-detail"),
    path("fuel-types/", CarFuelTypeListCreate.as_view(), name="carfueltype-list"),
    path("fuel-types/<int:pk>/", CarFuelTypeDetail.as_view(), name="carfueltype-detail"),
    path("transmission-types/", CarTransmissionTypeListCreate.as_view(), name="cartransmissiontype-list"),
    path(
        "transmission-types/<int:pk>/",
        CarTransmissionTypeDetail.as_view(),
        name="cartransmissiontype-detail",
    ),
]
