from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from listings.tests.factories import ListingFactory
from cars.tests.factories import CarBrandFactory

class ListingViewsTests(TestCase):
    def setUp(self):
        ListingFactory.create_batch(10, is_online=True,is_premium=True,hidden=False)
        ListingFactory.create_batch(10, is_online=False,is_premium=False,hidden=True)
        
    
    def test_get_listings(self):
        url = reverse("listing-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
    
    def test_filter_listings(self):
        brand = CarBrandFactory()
        ListingFactory(brand=brand, is_online=True, hidden=False)
        ListingFactory(brand=brand, is_online=True, hidden=False)
        
        ListingFactory(is_online=True, hidden=False)
        ListingFactory(is_online=True, hidden=False)
        

        url = reverse("listing-list")
        response = self.client.get(url, {"brand": [brand.id]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        