from django.contrib import admin
from django.urls import include, path
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from common.views import TestEmailView
from users.views import ProvinceList,ProvinceDetailUpdateDestroy,CityList,CityDetailUpdateDestroy,ZipCodeList,ZipCodeDetailUpdateDestroy

class ApiRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "listings": reverse("listing-list", request=request),
                "listings_control": reverse("listing-control", request=request),
                "users": reverse("user-list", request=request),
                "images": reverse("listing-image-create", request=request),
                "chats": reverse("chat-list", request=request),
                "messages": reverse("message-list", request=request),
                # temporary
                "locations": {
                    "provinces": reverse("province-list", request=request),
                    "cities": reverse("city-list", request=request),
                    "zipcodes": reverse("zip-list", request=request),
                    },
                "cars": {
                    "body_types": reverse("carbodytype-list", request=request),
                    "brands": reverse("carbrand-list", request=request),
                    "models": reverse("carmodel-list", request=request),
                    "trims": reverse("carmodeltrim-list", request=request),
                    "drive_trains": reverse("cardrivetrain-list", request=request),
                    "conditions": reverse("carcondition-list", request=request),
                },
            }
        )






urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", ApiRootView.as_view(), name="api-root"),
    path("api/test-email/", TestEmailView.as_view(), name="test-email"),
    path("api/listings/", include("listings.urls")),
    path("api/users/", include("users.urls")),
    path("api/cars/", include("cars.urls")),
    # temporary
    path("api/chat/", include("chat.urls"), name="chat"),
    path("api/province/", ProvinceList.as_view(), name="province-list"),
    path("api/province/<int:pk>/", ProvinceDetailUpdateDestroy.as_view(), name="province-detail"),
    path("api/city/", CityList.as_view(), name="city-list"),
    path("api/city/<int:pk>/", CityDetailUpdateDestroy.as_view(), name="city-detail"),
    path("api/zip/", ZipCodeList.as_view(), name="zip-list"),
    path("api/zip/<int:pk>/", ZipCodeDetailUpdateDestroy.as_view(), name="zip-detail"),

]
