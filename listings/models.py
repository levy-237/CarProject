from django.db import models
from cars.models import CarBrand,CarBodyType,CarModel,CarCondition,CarModelTrim
from users.models import User
from django.db.models import Q

def listing_image_upload_to(instance, filename):
    return f"listings/{instance.listing_id}/{filename}"


class ListingsManager(models.Manager):
    SELECT_RELATED_FIELDS = ["owner","brand","model","model_trim","model_trim__drivetrain","body_type","condition"]
    PREFETCH_RELATED_FIELDS = ["images","price_history"]
    
    def listing_optimization(self):
        return self.select_related(*self.SELECT_RELATED_FIELDS).prefetch_related(*self.PREFETCH_RELATED_FIELDS)
    
    
    #  only for internal use
    def everything(self):
        return self.listing_optimization().all()
    
    def online(self):
        return self.listing_optimization().filter(is_online=True, is_under_review=False).order_by("-is_premium","-publish_date")
    
    def offline(self):
        return self.listing_optimization().filter(is_online=False, is_under_review=False).order_by("-is_premium","-publish_date")

    def premium(self):
        return self.listing_optimization().filter(is_premium=True)
    
    def by_owner(self, user):
        return self.listing_optimization().filter(owner=user)
    
    def deactivated(self):
        return self.listing_optimization().filter(is_online=False)
    
    def is_under_review(self):
        return self.listing_optimization().filter(is_under_review=True)
    
    def for_advisor(self):
        return self.listing_optimization().filter(is_online=True, is_under_review=False).order_by("-is_premium")


    


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    publish_date = models.DateField(auto_now_add=True)
    title = models.TextField(max_length=2000)
    brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    model_trim = models.ForeignKey(CarModelTrim, on_delete=models.PROTECT,null=True,blank=True)
    makeyear = models.DateField()
    price = models.IntegerField()
    body_type = models.ForeignKey(CarBodyType, on_delete=models.PROTECT)
    mileage = models.IntegerField()
    condition = models.ForeignKey(CarCondition, on_delete=models.PROTECT)
    power = models.IntegerField()
    battery_health = models.IntegerField(null=True,blank=True)
    real_summer_range = models.IntegerField(null=True,blank=True)
    real_winter_range = models.IntegerField(null=True,blank=True)
    heat_pump = models.BooleanField(default=True)
    garantie = models.BooleanField(default=False)
    pickerl = models.BooleanField(default=False)
    description = models.TextField(max_length=2000)
    view_count = models.IntegerField(default=0)
    is_online = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=False)
    is_under_review = models.BooleanField(default=True)
    
    objects = ListingsManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="battery_health_validator",
                condition=(
                    Q(battery_health__isnull=True)
                    | (Q(battery_health__gte=0) & Q(battery_health__lte=100))
                ),
                violation_error_message="Battery health needs to be between 0 and 100",
            ),
            models.CheckConstraint(
                name="integer_values_validator",
                condition=(
                    Q(price__gte=0)
                    & Q(mileage__gte=1)
                    & Q(power__gte=1)
                    & Q(view_count__gte=0)
                    & (Q(real_summer_range__isnull=True) | Q(real_summer_range__gte=1))
                    & (Q(real_winter_range__isnull=True) | Q(real_winter_range__gte=1))
                ),
                violation_error_message="Integer values must be within their allowed ranges",
            ),
        ]

    def __str__(self):
        return f"car listing id: {self.pk} \n owner: {self.owner.username} - {self.owner.id}"


class ListingReport(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reports")
    reason = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_listings", null=True, blank=True)

    def __str__(self):
        return f"Report #{self.pk} for listing #{self.listing_id} ({self.reason})"

class Image(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.URLField(max_length=500)
    storage_key = models.CharField(max_length=255, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_cover = models.BooleanField(default=False)

    def __str__(self):
        return f"Image #{self.pk} for listing #{self.listing_id} ({self.storage_key})"
    
    
class PriceHistory(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="price_history")
    old_price = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Price history for listing #{self.listing_id} at {self.created_at}"
