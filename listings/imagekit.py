from django.conf import settings
from imagekitio import ImageKit
from rest_framework.exceptions import ValidationError


def get_imagekit_client():
    private_key = settings.IMAGEKIT_PRIVATE_KEY

    if not private_key:
        raise ValidationError({"imagekit": "Der private ImageKit-Schlüssel ist nicht konfiguriert."})

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
        raise ValidationError({"image": f"Der ImageKit-Upload ist fehlgeschlagen: {exc}"}) from exc

    url = response.url
    file_id = response.file_id

    if not url or not file_id:
        raise ValidationError({"image": "In der ImageKit-Upload-Antwort fehlen Dateidaten."})

    return response


def destroy_image(file_id):
    if not file_id:
        return

    try:
        get_imagekit_client().files.delete(file_id)
    except Exception as exc:
        raise ValidationError({"image": f"Das Löschen bei ImageKit ist fehlgeschlagen: {exc}"}) from exc
