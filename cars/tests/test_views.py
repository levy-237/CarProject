from rest_framework.test import APITestCase
from cars.tests.factories import CarBrandFactory
from users.tests.factories import UserFactory
from django.urls import reverse
from rest_framework import status

class CarModelsViewTests(APITestCase):
    def setUp(self):
        self.car_brand = CarBrandFactory(name="Test Car Brand")
        self.car_brand2 = CarBrandFactory(name="A Test Car Brand")
        
        

    def test_get_car_brand_list(self):
        response = self.client.get(reverse('carbrand-control-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], self.car_brand2.name)
        
    def test_get_car_brand_list_with_name_ordering(self):
        response = self.client.get(reverse('carbrand-control-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], self.car_brand2.name)
        
    def test_create_car_brand_by_staff(self):
        self.reg_user = UserFactory(is_staff=True,is_verified=True)
        self.client.force_authenticate(user=self.reg_user)
        response = self.client.post(reverse('carbrand-control-list'), {'name': 'Test Car Model'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Car Model')
        
    def test_create_car_brand_by_non_staff(self):
        self.reg_user = UserFactory(is_staff=False,is_verified=True)
        self.client.force_authenticate(user=self.reg_user)
        response = self.client.post(reverse('carbrand-control-list'), {'name': 'Test Car Model'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)