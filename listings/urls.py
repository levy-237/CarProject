
from django.urls import path

from .views import ListingCreateAndList, ListingDetailUpdateDelete, ListingImageCreateView, ListingByOwnerList, FavouriteListingUpdate, FavouriteListView       

urlpatterns = [
    path("", ListingCreateAndList.as_view(), name="listing-list"),
    path("<int:pk>/",ListingDetailUpdateDelete.as_view(), name="listing-detail"),
    path("my/", ListingByOwnerList.as_view(), name="listing-by-owner-list"),
    path("update-favourite/<int:pk>/", FavouriteListingUpdate.as_view(), name="favourite-list-update"),
    path("favourites/", FavouriteListView.as_view(), name="favourite-list"),
    path("images/", ListingImageCreateView.as_view(), name="listing-image-create"),
]
