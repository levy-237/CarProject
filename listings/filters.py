from datetime import date

import django_filters

from cars.models import (
    CarBodyType,
    CarBrand,
    CarCondition,
    CarFuelType,
    CarModel,
    CarTransmissionType,
)
from .models import Listing

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
    condition = django_filters.ModelMultipleChoiceFilter(
        field_name="condition", queryset=CarCondition.objects.all()
    )
    fuel = django_filters.ModelMultipleChoiceFilter(
        field_name="fuel", queryset=CarFuelType.objects.all()
    )
    transmission = django_filters.ModelMultipleChoiceFilter(
        field_name="transmission", queryset=CarTransmissionType.objects.all()
    )

    minprice = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    maxprice = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    minmileage = django_filters.NumberFilter(field_name="mileage", lookup_expr="gte")
    maxmileage = django_filters.NumberFilter(field_name="mileage", lookup_expr="lte")

    mindate = django_filters.NumberFilter(method="filter_min_year")
    maxdate = django_filters.NumberFilter(method="filter_max_year")

    class Meta:
        model = Listing
        fields = []

    def filter_min_year(self, queryset, name, value):
        return queryset.filter(makeyear__gte=date(int(value), 12, 31))

    def filter_max_year(self, queryset, name, value):
        return queryset.filter(makeyear__lte=date(int(value), 12, 31))
    