
from django.urls import path

from .views import ListingCreateAndList, ListingDetailAndUpdate, ListingImageCreateView, ListingByOwnerList

urlpatterns = [
    path("", ListingCreateAndList.as_view(), name="listing-list"),
    path("<int:pk>/",ListingDetailAndUpdate.as_view(), name="listing-detail"),
    path("mylistings/", ListingByOwnerList.as_view(), name="listing-by-owner-list"),
    path("images/", ListingImageCreateView.as_view(), name="listing-image-create"),
]
