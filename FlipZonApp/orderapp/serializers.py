from rest_framework import serializers
from .models import *


class OrderSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(read_only=True)
    day_order_no = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['address_distance'] > 10:
            raise serializers.ValidationError({"address_distance": "Distance can't be more than 10"})
        return data


    def create(self, validated_data):
        validated_data['order_number'], validated_data['day_order_no'] = get_latest_order_no()
        return super(OrderSerializer, self).create(validated_data)

    class Meta:
        model = Order
        fields = '__all__'


class ItemInventorySerializer(serializers.ModelSerializer):
    item_model_no = serializers.CharField(read_only=True, source="item.model_no")
    class Meta:
        model = ItemInventory
        fields = ('item_model_no', 'items_available', 'price')
    

class OrderDeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryInfo
        fields = ('order','team_assigned','delivery_start_at', \
            'estimated_delivery_at')