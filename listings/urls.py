
from django.urls import path

from .views import ListingCreateAndList, ListingDetailUpdateDelete, ListingImageCreateView, ListingImageDestroyView, ListingByOwnerList, ListingByOwnerDetailView, FavouriteListingUpdate, FavouriteListView, CompareListings,RecommendedListings, ListingControlListView, ListingControlDetailView, ListingManagementListView, ListingManagementDetailUpdateDelete, ListingReportCreateView, ListingReportList, ListingListCounter, ListingMostViewedView

urlpatterns = [
    path("", ListingCreateAndList.as_view(), name="listing-list"),
    path("<int:pk>/",ListingDetailUpdateDelete.as_view(), name="listing-detail"),
    path("count/", ListingListCounter.as_view(), name="listing-list-counter"),
    path("control/", ListingControlListView.as_view(), name="listing-control"),
    path("control/<int:pk>/", ListingControlDetailView.as_view(), name="listing-control-detail"),
    path("management/", ListingManagementListView.as_view(), name="listing-management"),
    path("management/<int:pk>/", ListingManagementDetailUpdateDelete.as_view(), name="listing-management-detail"),
    path("most-viewed/", ListingMostViewedView.as_view(), name="listing-most-viewed"),
    path("my/", ListingByOwnerList.as_view(), name="listing-by-owner-list"),
    path("my/<int:pk>/", ListingByOwnerDetailView.as_view(), name="listing-by-owner-detail"),
    path("update-favourite/<int:pk>/", FavouriteListingUpdate.as_view(), name="favourite-list-update"),
    path("favourites/", FavouriteListView.as_view(), name="favourite-list"),
    path("compare/", CompareListings.as_view(), name="compare-list"),
    path("recommend/", RecommendedListings.as_view(), name="recomended-list"),
    path("report/", ListingReportCreateView.as_view(), name="listing-report-create"),
    path("report-list/", ListingReportList.as_view(), name="listing-report-list"),
    path("images/", ListingImageCreateView.as_view(), name="listing-image-create"),
    path("images/<int:pk>/", ListingImageDestroyView.as_view(), name="listing-image-detail"),
]
