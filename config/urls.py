from django.contrib import admin
from django.urls import include, path
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from users.views import ProvinceList,ProvinceDetailUpdateDestroy,CityList,CityDetailUpdateDestroy
from common.mail_services import send_email

class ApiRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "listings": reverse("listing-list", request=request),
                "users": reverse("user-list", request=request),
                "images": reverse("listing-image-create", request=request),
                # temporary
                "locations": {
                    "provinces": reverse("province-list", request=request),
                    "cities": reverse("city-list", request=request),
                },
                "send_test_email": reverse("send-test-email", request=request),
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


class SendTestEmailView(APIView):
    def get(self, request, *args, **kwargs):
        mailgun_response = send_email()

        return Response(
            {
                "message": "Email request sent to Mailgun.",
                "mailgun_status_code": mailgun_response.status_code,
                "mailgun_response": mailgun_response.text,
            },
            status=mailgun_response.status_code,
        )





urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", ApiRootView.as_view(), name="api-root"),
    path("api/send-test-email/", SendTestEmailView.as_view(), name="send-test-email"),
    path("api/listings/", include("listings.urls")),
    path("api/users/", include("users.urls")),
    path("api/cars/", include("cars.urls")),
    # temporary
    path("api/province/", ProvinceList.as_view(), name="province-list"),
    path("api/province/<int:pk>/", ProvinceDetailUpdateDestroy.as_view(), name="province-detail"),
    path("api/city/", CityList.as_view(), name="city-list"),
    path("api/city/<int:pk>/", CityDetailUpdateDestroy.as_view(), name="city-detail"),

]
