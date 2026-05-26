from django.conf import settings
from imagekitio import ImageKit
from rest_framework.exceptions import ValidationError


def get_imagekit_client():
    private_key = settings.IMAGEKIT_PRIVATE_KEY

    if not private_key:
        raise ValidationError({"imagekit": "ImageKit private key is not configured."})

    return ImageKit(private_key=private_key)


def create_image(image_file):
    try:
        image_file.seek(0)
        response = get_imagekit_client().files.upload(
            file=image_file.read(),
            file_name=image_file.name,
            use_unique_file_name=True,
        )
    except Exception as exc:
        raise ValidationError({"image": f"ImageKit upload failed: {exc}"}) from exc

    url = response.url
    file_id = response.file_id

    if not url or not file_id:
        raise ValidationError({"image": "ImageKit upload response is missing file data."})

    return response


def destroy_image(file_id):
    if not file_id:
        return

    try:
        get_imagekit_client().files.delete(file_id)
    except Exception as exc:
        raise ValidationError({"image": f"ImageKit delete failed: {exc}"}) from exc
