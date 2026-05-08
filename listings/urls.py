
from django.urls import path

from .views import ListingCreateAndList, ListingDetailUpdateDelete, ListingImageCreateView, ListingImageDestroyView, ListingByOwnerList, FavouriteListingUpdate, FavouriteListView, CompareListings,RecommendedListings

urlpatterns = [
    path("", ListingCreateAndList.as_view(), name="listing-list"),
    path("<int:pk>/",ListingDetailUpdateDelete.as_view(), name="listing-detail"),
    path("my/", ListingByOwnerList.as_view(), name="listing-by-owner-list"),
    path("update-favourite/<int:pk>/", FavouriteListingUpdate.as_view(), name="favourite-list-update"),
    path("favourites/", FavouriteListView.as_view(), name="favourite-list"),
    path("compare/", CompareListings.as_view(), name="compare-list"),
    path("recomend/", RecommendedListings.as_view(), name="recomended-list"),
    path("images/", ListingImageCreateView.as_view(), name="listing-image-create"),
    path("images/<int:pk>/", ListingImageDestroyView.as_view(), name="listing-image-detail"),
]
