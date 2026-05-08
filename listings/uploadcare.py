import certifi
from django.conf import settings
from rest_framework.exceptions import ValidationError
from pyuploadcare import Uploadcare


def get_uploadcare_client():
    public_key = settings.UPLOADCARE_PUBLIC_KEY 
    secret_key = settings.UPLOADCARE_SECRET_KEY

    if not public_key or not secret_key:
        raise ValidationError({"uploadcare": "Uploadcare keys are not configured."})

    return Uploadcare(
        public_key=public_key,
        secret_key=secret_key,
        cdn_base=(settings.UPLOADCARE_CDN_BASE or "https://ucarecdn.com/").rstrip("/") + "/",
        verify_api_ssl=certifi.where(),
        verify_upload_ssl=certifi.where(),
    )
