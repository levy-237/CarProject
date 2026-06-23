from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from users.tests.factories import CityFactory, ProvinceFactory, UserFactory


class UserViewTests(APITestCase):
    def setUp(self):
        self.province = ProvinceFactory()

        self.city = CityFactory(province=self.province)

    @patch("users.views.send_email")
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
