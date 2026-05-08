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
        cdn_base=(settings.UPLOADCARE_CDN_BASE).rstrip("/") + "/",
        verify_api_ssl=certifi.where(),
        verify_upload_ssl=certifi.where(),
    )


def create_uploadcare_image(image_file):
    try:
        image_file.seek(0)
        uploadcare_client = get_uploadcare_client()
        uploadcare_file = uploadcare_client.upload(image_file,
                                                   size=image_file.size,
                                                   store=True)
    except Exception as exc:
        raise ValidationError({"image": f"Uploadcare upload failed: {exc}"}) from exc
    
    return uploadcare_file
        

def destroy_uploadcare_image(uploadcare_uuid):
    if uploadcare_uuid:
        try:
            get_uploadcare_client().file(uploadcare_uuid).delete()
        except Exception as exc:
            raise ValidationError({"image": f"Uploadcare delete failed: {exc}"}) from exc
