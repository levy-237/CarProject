from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image as PILImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from listings.models import Image
from listings.tests.factories import ImageFactory, ListingFactory
from users.tests.factories import UserFactory


def make_image_file(name="test.jpg"):
    buffer = BytesIO()
    PILImage.new("RGB", (10, 10), color="red").save(buffer, format="JPEG")
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type="image/jpeg")


class ImageViewTests(APITestCase):
    def setUp(self):
        self.owner = UserFactory(is_verified=True)
        self.listing = ListingFactory(owner=self.owner)

    @patch("listings.views.create_image")
    def test_owner_can_upload_image(self, mock_create_image):
        mock_create_image.return_value = SimpleNamespace(
            url="https://cdn.example.com/uploaded.jpg", file_id="uploaded-key-1"
        )
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            reverse("listing-image-create"),
            {"listing": self.listing.id, "image": make_image_file()},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        image = Image.objects.first()
        self.assertEqual(image.image, "https://cdn.example.com/uploaded.jpg")
        self.assertEqual(image.storage_key, "uploaded-key-1")

    @patch("listings.views.destroy_image")
    def test_owner_can_delete_image(self, mock_destroy_image):
        image = ImageFactory(listing=self.listing, storage_key="delete-key-1")
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(reverse("listing-image-detail", args=[image.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Image.objects.filter(id=image.id).exists())
        mock_destroy_image.assert_called_once_with("delete-key-1")
