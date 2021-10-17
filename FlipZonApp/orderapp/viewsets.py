import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseBadRequest


from .models import *
from . import serializers
from . import filters


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_class = filters.OrderFilter

    def create(self, request, *args, **kwargs):
        '''
        Also creates the OrderItemCount objects for particular order
        '''
        item_list = request.data.get('item_list')

        item_count_dict = {}
        for item_dict in item_list:
            model = item_dict['model_number']
            quantity_ordered = int(item_dict['quantity'])
            try:
                item = Item.objects.get(model_no=model)
            except Item.DoesNotExist:
                error_message = 'Item model number Invalid'
                return HttpResponseBadRequest(json.dumps(
                    {"Error": error_message}), content_type='application/json')

            item_inventory = ItemInventory.objects.get(item=item).items_available
            if item_inventory >= quantity_ordered:
                item_count_dict[item] = quantity_ordered
            else:
                error_message = 'Inventory left for item {} is {}'.format(
                        model, str(item_inventory))
                return HttpResponseBadRequest(json.dumps(
                    {"Error": error_message}), content_type='application/json')


        # finally creating the order 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        order_obj = Order.objects.get(order_number=serializer.data['order_number'])

        for item, quantity in item_count_dict.items():
            OrderItemCount.objects.create(
                order=order_obj,
                item=item,
                count=quantity,                   
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ItemInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ItemInventory.objects.all()
    serializer_class = serializers.ItemInventorySerializer
    filter_class = filters.ItemInventoryFilter


class OrderDeliveryInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderDeliveryInfo.objects.all()
    serializer_class = serializers.OrderDeliveryInfoSerializer
    filter_class = filters.OrderDeliveryInfoFilter
