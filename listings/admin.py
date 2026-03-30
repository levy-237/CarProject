from django.contrib import admin
from .models import Image, Listing
# Register your models here.

admin.site.register(Listing)
admin.site.register(Image)