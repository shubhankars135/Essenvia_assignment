from django_filters import rest_framework as filters

from .models import *



COMPARE_FILTERS = ['lte', 'gte', 'lt', 'gt', 'exact']
APPROX_MATCH_FILTERS = ['exact', 'startswith', 'contains', 'in']
MATCH_FILTERS = ['exact']


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'order_number': MATCH_FILTERS,
            'timestamp': COMPARE_FILTERS,
        }

class ItemInventoryFilter(filters.FilterSet):
    class Meta:
        model = ItemInventory
        fields = {
            'item': MATCH_FILTERS,
            'item_id': MATCH_FILTERS,
        }


class OrderDeliveryInfoFilter(filters.FilterSet):
    class Meta:
        model = OrderDeliveryInfo
        fields = {
            'order': MATCH_FILTERS,
        }


