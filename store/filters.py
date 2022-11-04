import django_filters
from .models import *
from django_filters import DateFilter, RangeFilter, NumberFilter


class ProductFilter(django_filters.FilterSet):
    price__gt=NumberFilter(field_name='price', lookup_expr='gt')
    price__lt=NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model=Product
        fields='__all__'
        exclude = ['image', 'seller', 'digital', 'Description', 'product_date', 'price', 'stock', 'pop_count']
