from django.test import TestCase
from listings.models import Listing
from users.models import User
from listings.tests.factories import ListingFactory
from users.tests.factories import UserFactory
from cars.tests.factories import CarBrandFactory, CarModelFactory, CarBodyTypeFactory, CarConditionFactory, CarDriveTrainFactory
from cars.models import CarBrand, CarModel, CarBodyType, CarCondition, CarDriveTrain
from datetime import date
class ListingModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.brand = CarBrandFactory()
        self.model = CarModelFactory(connected_brand=self.brand)
        self.body_type = CarBodyTypeFactory()
        self.condition = CarConditionFactory()
        self.drivetrain = CarDriveTrainFactory()
        self.price = 25000
        self.mileage = 10000
        self.power = 100
        self.makeyear = date(2020, 1, 1)
        self.publish_date = date.today()
 
        self.listing = ListingFactory(
            owner=self.user,
            brand=self.brand,
            model=self.model,
            body_type=self.body_type,
            condition=self.condition,
            drivetrain=self.drivetrain,
            makeyear=self.makeyear,
            price=self.price,
            mileage=self.mileage,
            power=self.power,
            is_online=True,
            is_premium=True,
            hidden=False,
        )
        self.listing2 = ListingFactory(
            owner=self.user2,
            brand=self.brand,
            model=self.model,
            body_type=self.body_type,
            condition=self.condition,
            drivetrain=self.drivetrain,
            makeyear=self.makeyear,
            price=self.price,
            mileage=self.mileage,
            power=self.power,
            is_online=False,
            is_premium=False,
            hidden=True,
        )
        
    def test_create_listing_and_default_values(self):
        self.assertEqual(self.listing.owner, self.user)
        self.assertEqual(self.listing.brand, self.brand)
        self.assertEqual(self.listing.model, self.model)
        self.assertEqual(self.listing.makeyear, date(2020, 1, 1))
        self.assertEqual(self.listing.price, 25000)
        self.assertEqual(self.listing.mileage, 10000)
        self.assertEqual(self.listing.power, 100)
        self.assertEqual(self.listing.body_type, self.body_type)
        self.assertEqual(self.listing.condition, self.condition)
        self.assertEqual(self.listing.drivetrain, self.drivetrain)
        self.assertEqual(self.listing.is_online, True)
        self.assertEqual(self.listing.is_premium, True)
        self.assertEqual(self.listing.hidden, False)
        self.assertEqual(self.listing2.is_online, False)
        self.assertEqual(self.listing2.is_premium, False)
        self.assertEqual(self.listing2.hidden, True)
        self.assertEqual(self.listing2.publish_date, date.today())
        self.assertEqual(self.listing.publish_date, date.today())
        
    def test_listing_manager(self):
        online_listings = Listing.objects.online()
        premium_listings = Listing.objects.premium()
        not_hidden_listings = Listing.objects.not_hidden()
        owned_listings = Listing.objects.by_owner(self.user)
        hidden_listings = Listing.objects.hidden()
        
        self.assertIn(self.listing, online_listings)
        self.assertIn(self.listing, premium_listings)
        self.assertIn(self.listing, not_hidden_listings)
        self.assertIn(self.listing, owned_listings)
        self.assertNotIn(self.listing2, online_listings)
        self.assertNotIn(self.listing2, premium_listings)
        self.assertNotIn(self.listing2, not_hidden_listings)
        self.assertNotIn(self.listing2, owned_listings)
        self.assertIn(self.listing2, hidden_listings)
        self.assertNotIn(self.listing, hidden_listings)
    
    def test_listing_str(self):
        self.assertEqual(str(self.listing), f"car listing id: {self.listing.id} \n owner: {self.listing.owner.username} - {self.listing.owner.id}")
        
        
        
    def test_listing_is_deleted_when_owner_is_deleted(self):
        listing_id = self.listing.id
        self.user.delete()
        self.assertFalse(Listing.objects.filter(id=listing_id).exists())
