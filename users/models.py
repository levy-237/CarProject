from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=40,blank=True,null=True)
    last_name = models.CharField(max_length=70,blank=True,null=True)
    picture = models.URLField(max_length=500,blank=True,null=True)
    uploadcare_uuid = models.CharField(max_length=36, blank=True, db_index=True,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True,null=True)
    favourite_listings = models.ManyToManyField(
    "listings.Listing",
    related_name="favorited_by",
    blank=True,
    )
    