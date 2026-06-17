from rest_framework import status
from django.urls import reverse
from listings.tests.factories import ListingFactory
from listings.models import Listing, PriceHistory
from cars.tests.factories import CarBrandFactory,CarModelFactory,CarBodyTypeFactory,CarConditionFactory,CarModelTrimFactory
from users.tests.factories import UserFactory
from rest_framework.test import APITestCase
from datetime import date

class ListingViewsTests(APITestCase):
    def setUp(self):
        # ListingFactory.create_batch(10, is_online=True,is_premium=True,is_under_review=False)
        # ListingFactory.create_batch(10, is_online=False,is_premium=False,is_under_review=True)
        self.url = reverse("listing-list")
        self.user_2 = UserFactory(is_verified=True)
        self.brand = CarBrandFactory()
        self.model = CarModelFactory(connected_brand=self.brand)  
        self.model_trim = CarModelTrimFactory(connected_model=self.model)
        self.body_type = CarBodyTypeFactory()
        self.condition = CarConditionFactory()   
        self.description = "This is a test listing"
        self.title = "This is a test title"
        self.makeyear = date(2020, 1, 1)
        self.price = 25000
        self.mileage = 10000
        self.power = 150
        self.payload = {
            "brand": self.brand.id,
            "model": self.model.id,
            "model_trim": self.model_trim.id,
            "body_type": self.body_type.id,
            "condition": self.condition.id,
            "makeyear": self.makeyear,
            "price": self.price,
            "mileage": self.mileage,
            "power": self.power,
            "title": self.title,
            "description": self.description,
        } 
        
    
    def test_can_verified_user_create_listing(self):  
        verified_user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=verified_user)
        
        response = self.client.post(self.url,self.payload,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["brand"], self.brand.id)
        self.assertEqual(response.data["model"], self.model.id)
        self.assertEqual(response.data["model_trim"], self.model_trim.id)
        self.assertEqual(response.data["body_type"], self.body_type.id)
        self.assertEqual(response.data["condition"], self.condition.id)
        self.assertEqual(response.data["makeyear"], self.makeyear.isoformat())
        self.assertEqual(response.data["price"], self.price)
        self.assertEqual(response.data["mileage"], self.mileage)
        self.assertEqual(response.data["power"], self.power)
        self.assertEqual(response.data["description"], self.description)
        self.assertEqual(Listing.objects.count(), 1)
        
        
    def test_can_non_verified_user_create_listing(self):
        non_verified_user = UserFactory(is_verified=False)
        self.client.force_authenticate(user=non_verified_user)
        
        response = self.client.post(self.url,self.payload,format="json")
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Listing.objects.count(), 0)
        
        
    def test_can_non_auth_user_create_listing(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url,self.payload,format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Listing.objects.count(), 0)
        
    def test_can_owner_update_listing(self):
        owner = UserFactory(is_verified=True)
        self.client.force_authenticate(user=owner)
        listing = ListingFactory(owner=owner)
        url = reverse("listing-detail", args=[listing.id])
        response = self.client.put(url,self.payload,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["brand"], self.brand.id)
        self.assertEqual(response.data["model"], self.model.id)
        self.assertEqual(response.data["model_trim"], self.model_trim.id)
        self.assertEqual(response.data["body_type"], self.body_type.id)
        self.assertEqual(response.data["condition"], self.condition.id)
        self.assertEqual(response.data["makeyear"], self.makeyear.isoformat())
        
    def test_can_not_owner_update_listing(self):
        user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=user)
        listing = ListingFactory(owner=self.user_2)
        
        url = reverse("listing-detail", args=[listing.id])
        response = self.client.put(url,self.payload,format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_can_owner_delete_listing(self):
        owner = UserFactory(is_verified=True)
        self.client.force_authenticate(user=owner)
        listing = ListingFactory(owner=owner)
        url = reverse("listing-detail", args=[listing.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Listing.objects.count(), 0)
        
    def test_can_not_owner_delete_listing(self):
        user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=user)
        listing = ListingFactory(owner=self.user_2)
        url = reverse("listing-detail", args=[listing.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Listing.objects.count(), 1)
        
    def test_can_staff_delete_listing(self):
        staff = UserFactory(is_verified=True,is_staff=True)
        self.client.force_authenticate(user=staff)
        listing = ListingFactory(owner=self.user_2)
        url = reverse("listing-detail", args=[listing.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Listing.objects.count(), 0)
        
        
    def test_can_staff_update_listing(self):
        staff = UserFactory(is_verified=True,is_staff=True)
        self.client.force_authenticate(user=staff)
        listing = ListingFactory(owner=self.user_2)
        url = reverse("listing-detail", args=[listing.id])
        response = self.client.put(url,self.payload,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["brand"], self.brand.id)
        self.assertEqual(response.data["model"], self.model.id)
        
    
    def test_created_listing_goes_under_review(self):
        verified_user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=verified_user)
        response = self.client.post(self.url,self.payload,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.first().is_under_review, True)
        self.assertEqual(Listing.objects.first().is_online, False)
        
    def test_created_listing_cant_bypass_review(self):
        verified_user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=verified_user)
        self.payload["is_under_review"] = False
        self.payload["is_online"] = True
        
        response = self.client.post(self.url,self.payload,format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.first().is_under_review, True)
        self.assertEqual(Listing.objects.first().is_online, False)
    
    def test_under_review_listing_is_not_online(self):
        verified_user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=verified_user)
        
        response = self.client.post(self.url,self.payload,format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.online().count(), 0)
        
    
    def test_listing_view_count_increments(self):
        verified_user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=verified_user)
        listing = ListingFactory(is_online=True,is_under_review=False)
        url = reverse("listing-detail", args=[listing.id])
        
        self.client.get(url)
        
        self.assertEqual(Listing.objects.first().view_count,1)
        
    def test_price_history_update(self):
        verified_user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=verified_user)
        listing = ListingFactory(owner=verified_user,is_online=True,is_under_review=False)
        
        url = reverse("listing-detail",args=[listing.id])
        self.client.patch(url,{"price":500})
        
        old_price_for_test = listing.price_history.first().old_price
        
        self.assertEqual(PriceHistory.objects.count(),1)
        self.assertEqual(old_price_for_test, listing.price)
    
    def test_can_unverified_favourite_listing(self):
        unverified_user = UserFactory(is_verified=False)
        self.client.force_authenticate(user=unverified_user)
        listing_1 = ListingFactory(is_online=True, is_under_review=False)
        
        url = reverse("favourite-list-update",args=[listing_1.id])
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_can_non_auth_favourite_listing(self):
        self.client.force_authenticate(user=None)
        listing_1 = ListingFactory(is_online=True,is_under_review=False)
        
        url = reverse("favourite-list-update",args=[listing_1.id])
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
        
    def test_can_owner_favourite_listing(self):
        verified_user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=verified_user)
        listing_1 = ListingFactory(owner=verified_user, is_online=True,is_under_review=False)
        
        url = reverse("favourite-list-update",args=[listing_1.id])
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
    def test_favourite_listing_add_and_delete(self):
        verified_user = UserFactory(is_verified=True)
        self.client.force_authenticate(user=verified_user)
        listing_1 = ListingFactory(is_online=True,is_under_review=False)
        listing_2 = ListingFactory(is_online=True,is_under_review=False)
        
        url_listing_1 = reverse("favourite-list-update",args=[listing_1.id])
        url_listing_2 = reverse("favourite-list-update",args=[listing_2.id])
        
        self.client.post(url_listing_1)
        self.client.post(url_listing_2)
        self.client.post(url_listing_1)
        
        
        
        self.assertEqual(verified_user.favourite_listings.count(),1)
        self.assertEqual(verified_user.favourite_listings.first(),listing_2)
        
        
        
        
        
    
    
    # def test_get_listings(self):
    #     url = reverse("listing-control")
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data["results"]), 10)
    
    # def test_filter_listings(self):
    #     brand = CarBrandFactory()
    #     model = CarModelFactory(connected_brand=brand)
        
    #     ListingFactory(brand=brand, is_online=True)
    #     ListingFactory(brand=brand, is_online=True)
        
    #     ListingFactory(is_online=True)
    #     ListingFactory(is_online=True)
        

    #     url = reverse("listing-list")
    #     response = self.client.get(url, {"brand": [brand.id]})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data["results"]), 2)
        