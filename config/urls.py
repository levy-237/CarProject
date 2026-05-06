from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from listings.views import ProvinceList,ProvinceDetailUpdateDestroy,CityList,CityDetailUpdateDestroy

class ApiRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "listings": reverse("listing-list", request=request),
                "users": reverse("user-list", request=request),
                "cars": {
                    "body_types": reverse("carbodytype-list", request=request),
                    "brands": reverse("carbrand-list", request=request),
                    "models": reverse("carmodel-list", request=request),
                    "conditions": reverse("carcondition-list", request=request),
                    "fuel_types": reverse("carfueltype-list", request=request),
                    "transmission_types": reverse(
                        "cartransmissiontype-list", request=request
                    ),
                },
            }
        )





urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", ApiRootView.as_view(), name="api-root"),
    path("api/listings/", include("listings.urls")),
    path("api/users/", include("users.urls")),
    path("api/cars/", include("cars.urls")),
    path("api/province/", ProvinceList.as_view(), name="province-list"),
    path("api/province/<int:pk>/", ProvinceDetailUpdateDestroy.as_view(), name="province-detail"),
    path("api/city/", CityList.as_view(), name="city-list"),
    path("api/city/<int:pk>/", CityDetailUpdateDestroy.as_view(), name="city-detail"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
