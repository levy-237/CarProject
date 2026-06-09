from django.contrib.auth.models import AbstractUser
from django.db import models



class Province(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    

class City(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT,related_name="connected_cities")
    
    
    
    def __str__(self):
        return self.name
    
class ZipCode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10)
    cities = models.ManyToManyField(City,related_name="zipcodes",blank=True)



class User(AbstractUser):
    created_at = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=70)
    company_name = models.CharField(max_length=100,blank=True,null=True)
    picture = models.URLField(max_length=500,blank=True,null=True)
    storage_key = models.CharField(max_length=255, blank=True, db_index=True,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=40, blank=True,null=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    streetname_number = models.CharField(max_length=100, blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=128, blank=True,null=True)
    email_verification_code_date = models.DateTimeField(blank=True,null=True)
    password_recovery_code = models.CharField(max_length=128, blank=True,null=True)
    password_recovery_code_date = models.DateTimeField(blank=True,null=True)
    is_private = models.BooleanField()
    favourite_listings = models.ManyToManyField(
    "listings.Listing",
    related_name="favourited_by",
    blank=True,
    )

    
class savedSearch(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_search")
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    saved_url = models.CharField(max_length=500)
    
    
    def __str__(self):
        return self.saved_url
    