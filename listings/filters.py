from datetime import date

import django_filters
from django.db.models import Q, Case, When, Value, IntegerField

from cars.models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarDriveTrain,
    CarModel,
    CarModelTrim
)
from .models import Listing
from users.models import City, Province

class ListingFilter(django_filters.FilterSet):
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name="brand", queryset=CarBrand.objects.all()
    )
    body = django_filters.ModelMultipleChoiceFilter(
        field_name="body_type", queryset=CarBodyType.objects.all()
    )
    model = django_filters.ModelMultipleChoiceFilter(
        field_name="model", queryset=CarModel.objects.all()
    )
    modeltrim = django_filters.ModelMultipleChoiceFilter(
        field_name="model_trim", queryset=CarModelTrim.objects.all()
    )
    condition = django_filters.ModelMultipleChoiceFilter(
        field_name="condition", queryset=CarCondition.objects.all()
    )
    drivetrain = django_filters.ModelMultipleChoiceFilter(
        field_name="model_trim__drivetrain", queryset=CarDriveTrain.objects.all()
    )
    city = django_filters.ModelMultipleChoiceFilter(
        field_name="owner__city", queryset=City.objects.all()
    )
    province = django_filters.ModelMultipleChoiceFilter(
        field_name="owner__province", queryset=Province.objects.all()
    )
    
    minprice = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxprice = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    
    minmileage = django_filters.NumberFilter(field_name="mileage", lookup_expr="gte")
    maxmileage = django_filters.NumberFilter(field_name="mileage", lookup_expr="lte")
    
    minpower = django_filters.NumberFilter(field_name="power", lookup_expr="gte")
    maxpower = django_filters.NumberFilter(field_name="power", lookup_expr="lte")
    
    minbattery = django_filters.NumberFilter(field_name="model_trim__battery_size", lookup_expr="gte")
    maxbattery = django_filters.NumberFilter(field_name="model_trim__battery_size", lookup_expr="lte")
    
    minfactoryrange = django_filters.NumberFilter(field_name="model_trim__factory_range", lookup_expr="gte")
    maxfactoryrange = django_filters.NumberFilter(field_name="model_trim__factory_range", lookup_expr="lte")
    
    minsummerrange = django_filters.NumberFilter(field_name="real_summer_range", lookup_expr="gte")
    maxsummerrange = django_filters.NumberFilter(field_name="real_summer_range", lookup_expr="lte")
    
    minwinterrange = django_filters.NumberFilter(field_name="real_winter_range", lookup_expr="gte")
    maxwinterrange = django_filters.NumberFilter(field_name="real_winter_range", lookup_expr="lte")
    
    minaccharging = django_filters.NumberFilter(field_name="model_trim__max_ac_charge_kw", lookup_expr="gte")
    mindccharging = django_filters.NumberFilter(field_name="model_trim__max_dc_charge_kw", lookup_expr="gte")
    maxfastcharginmin = django_filters.NumberFilter(field_name="model_trim__twenty_to_eighty_charge_min", lookup_expr="lte")
    
    garantie = django_filters.BooleanFilter(field_name="garantie")
    pickerl = django_filters.BooleanFilter(field_name="pickerl")
    heatpump = django_filters.BooleanFilter(field_name="heat_pump")

    mindate = django_filters.NumberFilter(method="filter_min_year")
    maxdate = django_filters.NumberFilter(method="filter_max_year")
    search = django_filters.CharFilter(method="filter_search")


    class Meta:
        model = Listing
        fields = []

    def filter_min_year(self, queryset, name, value):
        return queryset.filter(makeyear__gte=date(int(value), 1, 1))

    def filter_max_year(self, queryset, name, value):
        return queryset.filter(makeyear__lte=date(int(value), 12, 31))
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
              Q(title__icontains=value) |
              Q(description__icontains=value) |
              Q(body_type__name__icontains=value) |
              Q(brand__name__icontains=value) |
              Q(model__name__icontains=value) |
              Q(model_trim__drivetrain__name__icontains=value) |
              Q(owner__city__name__icontains=value) |
              Q(owner__province__name__icontains=value)
              ).annotate(
                 match_priority=Case(
                 When(title__icontains=value, then=Value(0)),
                 When(description__icontains=value, then=Value(1)),
                 When(body_type__name__icontains=value, then=Value(2)),
                 default=Value(99),
                 output_field=IntegerField(),
                )
            ).order_by("match_priority").distinct()
    