
from django.urls import path

from .views import ListCreateAndList

urlpatterns = [
    path("", ListCreateAndList.as_view(), name="listing-list"),

]
