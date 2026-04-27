from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True,null=True)
    favourite_listings = models.ManyToManyField(
    "listings.Listing",
    related_name="favorited_by",
    blank=True,
)
    