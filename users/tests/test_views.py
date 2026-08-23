from io import BytesIO
from unittest import skipUnless
from unittest.mock import patch

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image as PILImage
from rest_framework import status
from rest_framework.test import APITestCase

from listings.imagekit import destroy_image
from users.models import User
from listings.models import Image
from users.tests.factories import CityFactory, ProvinceFactory, UserFactory


def make_image_file(name="profile.jpg"):
    buffer = BytesIO()
    PILImage.new("RGB", (10, 10), color="red").save(buffer, format="JPEG")
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type="image/jpeg")


class UserViewTests(APITestCase):
    def setUp(self):
        self.province = ProvinceFactory()

        self.city = CityFactory(province=self.province)
        self.user_with_image_payload = {
            "username": "imageuser",
            "first_name": "Image",
            "last_name": "User",
            "email": "imageuser@example.com",
            "password": "testpassword123",
            "province": self.province.id,   
            "city": self.city.id,
            "is_private": True,
            "picture_file": make_image_file(),
        }

    @patch("users.views.send_email_safely")
    def test_register_creates_user(self, mock_send_email):
        payload = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password": "testpassword123",
            "province": self.province.id,
            "city": self.city.id,
            "is_private": True,
        }

        response = self.client.post(reverse("user-register"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        mock_send_email.assert_called_once()

    @skipUnless(settings.IMAGEKIT_PRIVATE_KEY, "ImageKit is not configured.")
    @patch("users.views.send_email_safely")
    def test_register_creates_user_with_profile_image(self, mock_send_email):


        response = self.client.post(reverse("user-register"), self.user_with_image_payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="imageuser@example.com")
        self.addCleanup(destroy_image, user.storage_key)
        self.assertTrue(user.picture)
        self.assertTrue(user.storage_key)
        mock_send_email.assert_called_once()

    @skipUnless(settings.IMAGEKIT_PRIVATE_KEY, "ImageKit is not configured.")
    @patch("users.views.send_email_safely")
    def test_delete_user_with_profile_image(self, mock_send_email):
    

        register_response = self.client.post(
            reverse("user-register"),
            self.user_with_image_payload,
            format="multipart",
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="deleteimageuser@example.com")
        self.assertTrue(user.storage_key)
        self.assertTrue(Image.objects.filter(storage_key=user.storage_key).exists())
        mock_send_email.assert_called_once()

        self.client.force_authenticate(user=user)
        delete_response = self.client.delete(reverse("user-detail", args=[user.id]))
        
        self.assertFalse(Image.objects.filter(storage_key=user.storage_key).exists())
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user.id).exists())

    def test_me_returns_current_user(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse("user-me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["email"], user.email)

    def test_city_list_filters_by_province(self):
        other_province = ProvinceFactory()
        other_city = CityFactory(province=other_province)

        response = self.client.get(reverse("city-list"), {"relation": self.province.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        city_ids = [city["id"] for city in response.data["results"]]
        self.assertIn(self.city.id, city_ids)
        self.assertNotIn(other_city.id, city_ids)
        
    def test_company_list_returns_companies(self):
        UserFactory.create_batch(10, is_private=False)
        UserFactory.create_batch(10, is_private=True)
        
        response = self.client.get(reverse("user-company-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    @patch("users.views.send_email_safely")
    def test_recovery_request_does_not_reveal_if_email_exists(self, mock_send_email):
        user = UserFactory()

        existing_response = self.client.post(
            reverse("send-user-password-recovery"),
            {"email": user.email},
            format="json",
        )
        missing_response = self.client.post(
            reverse("send-user-password-recovery"),
            {"email": "missing@example.com"},
            format="json",
        )

        self.assertEqual(existing_response.status_code, status.HTTP_200_OK)
        self.assertEqual(missing_response.status_code, status.HTTP_200_OK)
        self.assertEqual(existing_response.data, missing_response.data)
        self.assertEqual(
            existing_response.data,
            {
                "message": "Falls ein Konto mit dieser E-Mail-Adresse existiert, wurde ein Wiederherstellungscode gesendet."
            },
        )

    def test_recovery_attempt_does_not_reveal_if_email_exists(self):
        user = UserFactory()
        payload = {"new_password": "NewSecurePassword123!", "code": "123456"}

        existing_response = self.client.post(
            reverse("user-password-recovery"),
            {"email": user.email, **payload},
            format="json",
        )
        missing_response = self.client.post(
            reverse("user-password-recovery"),
            {"email": "missing@example.com", **payload},
            format="json",
        )

        self.assertEqual(existing_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(missing_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(existing_response.data, missing_response.data)
        self.assertEqual(
            existing_response.data,
            {
                "detail": "E-Mail-Adresse oder Wiederherstellungscode ist ungültig oder abgelaufen."
            },
        )
