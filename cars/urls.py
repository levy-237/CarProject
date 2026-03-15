
from django.urls import path

from .views import CarCreateAndList, CarViewAndUpdate

urlpatterns = [
    path("", CarCreateAndList.as_view(), name="car-list"),
    path("<int:pk>/", CarViewAndUpdate.as_view(), name="car-detail"),
]
