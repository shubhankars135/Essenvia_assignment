import datetime as dt
import json
import pytz
import pandas as pd


from django.shortcuts import render
from django.http import HttpResponse

from .models import *

# Create your views here.

# fetch order number from backend
# check inventory status
# check order confirmation status
# fetch Estimated time of delivery

def get_order_no(request):
    """
    Gets the next order number
    """
    order_number = get_latest_order_no()[0]
    result = {'order_no':order_number}
    return HttpResponse(json.dumps(result), content_type='application/json')


def generate_day_report(request):
    '''
    Return html for todays Orders
    '''
    ist = pytz.timezone('Asia/Kolkata')
    current_date = dt.datetime.now().astimezone(ist).date()

    order_item_query = OrderItemCount.objects.filter(
        order__timestamp__date=current_date)
    if order_item_query.exists():
        order_item_df = pd.DataFrame(order_item_query.values())

        order_item_df['price'] = order_item_df.apply(lambda row: \
            ItemInventory.objects.get(item_id=row['item_id']).price, axis=1) 

        order_item_df['Amount'] = order_item_df['price'] * order_item_df['count'] 

        order_item_df = order_item_df.groupby('order_id', as_index=False).agg(
            {'Amount': 'sum'}) 

        order_item_df['Estimated Delivery Time'] = order_item_df.apply(
            lambda row: OrderDeliveryInfo.objects.get(order__order_number= \
                row['order_id']).estimated_delivery_at.astimezone(ist).strftime('%I:%M %p'), axis=1)
        order_item_df.rename(columns={'order_id':'Order ID'}, inplace=True)      
        result = order_item_df.to_html(index=False)
    else:
        result = 'No data'
    return HttpResponse(result)


def fill_inventory(request):
    '''
    This resets the inventory or fills it for the first time with values given in \
    problem statement

    Category          Model No     Available    Price (Rs)
    Television   T2020UHD               1         38999
                 T20214K                3         45449
    Refrigerator R260LCS                0         21449
                 R395LIL                2         35999    
    '''
    #Item.objects.all().delete()
    ItemInventory.objects.all().delete()
    DeliveryTeamInfo.objects.all().delete()

    item_obj1, created = Item.objects.get_or_create(category='Television',model_no='T2020UHD')
    item_obj2, created = Item.objects.get_or_create(category='Television',model_no='T20214K')
    item_obj3, created = Item.objects.get_or_create(category='Refrigerator',model_no='R260LCS')
    item_obj4, created = Item.objects.get_or_create(category='Refrigerator',model_no='R395LIL')

    ItemInventory.objects.create(item=item_obj1 , price= 38999, items_available=1)
    ItemInventory.objects.create(item=item_obj2 , price= 45449, items_available=3)
    ItemInventory.objects.create(item=item_obj3 , price= 21449, items_available=0)
    ItemInventory.objects.create(item=item_obj4 , price= 35999, items_available=2)

    ist = pytz.timezone('Asia/Kolkata')
    yesterday = (dt.datetime.now().astimezone(ist) - dt.timedelta(days=1)).date()
    yesterday = dt.datetime.combine(yesterday, dt.time(0,0))

    DeliveryTeamInfo.objects.create(team='a', latest_delivery_complete_at=yesterday)
    DeliveryTeamInfo.objects.create(team='b', latest_delivery_complete_at=yesterday)

    result = {'Status':'Success'}
    return HttpResponse(json.dumps(result),
        content_type='application/json')
