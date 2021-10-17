from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','customer_name','customer_address', \
        'timestamp','day_order_no')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass 


@admin.register(ItemInventory)
class ItemInventoryAdmin(admin.ModelAdmin):
    list_display = ('item','price','items_available')
 


@admin.register(OrderItemCount)
class OrderItemCountAdmin(admin.ModelAdmin):
    list_display = ('order','item','count')


@admin.register(DeliveryTeamInfo)
class DeliveryTeamInfoAdmin(admin.ModelAdmin):
    list_display = ('team','latest_delivery_complete_at')

@admin.register(OrderDeliveryInfo)
class OrderDeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ('order','team_assigned','delivery_start_at', \
        'estimated_delivery_at','actual_delivery_at','estimated_return_at', \
        'actual_return_at')
