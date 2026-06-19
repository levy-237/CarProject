from django.test import TestCase

from users.models import savedSearch
from users.tests.factories import CityFactory, ProvinceFactory, UserFactory


class UserModelTests(TestCase):
    def test_user_factory_defaults(self):
        user = UserFactory()

        # New users start unverified and as a company account (is_private=False).
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_private)
        # The factory hashes the password, so check_password (not ==) must pass.
        self.assertTrue(user.check_password("testpassword123"))

    def test_saved_search_str(self):
        user = UserFactory()
        saved = savedSearch.objects.create(
            owner=user, name="My search", saved_url="?brand=tesla"
        )

        self.assertEqual(str(saved), "?brand=tesla")


class LocationModelTests(TestCase):
    def test_city_belongs_to_province(self):
        province = ProvinceFactory()
        city = CityFactory(province=province)

        self.assertEqual(city.province, province)
        # The reverse relation is exposed via related_name="connected_cities".
        self.assertIn(city, province.connected_cities.all())

    def test_province_str(self):
        province = ProvinceFactory(name="Vienna")

        self.assertEqual(str(province), "Vienna")
