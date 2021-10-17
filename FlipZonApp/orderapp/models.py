import datetime as dt

from django.db import models
from django.db.models import Max

# Create your models here.


class Order(models.Model):
    order_number = models.CharField(primary_key=True, max_length=30)
    customer_name = models.CharField(max_length=50)
    customer_address = models.CharField(max_length=100)
    address_distance = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    day_order_no = models.IntegerField()


class Item(models.Model):
    category = models.CharField(max_length=50)
    model_no = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.model_no


class ItemInventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, unique=True)
    price = models.FloatField()
    items_available = models.IntegerField()


class OrderItemCount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField()

    class Meta:
        unique_together = ('order', 'item')


    def save(self, *args, **kwargs):
        items_inventory = ItemInventory.objects.get(item=self.item)
        current_avaialble = items_inventory.items_available - self.count
        if current_avaialble >= 0:
            items_inventory.items_available = current_avaialble
            items_inventory.save()
        
            super(OrderItemCount, self).save(*args, **kwargs)
        else :
            raise ValueError('Only {} items left for item {}'.format(
                str(self.count), item.model_no))


TEAMS_CHOICES = (
    ('a', 'Team A'),
    ('b', 'Team B')    
)   


class DeliveryTeamInfo(models.Model):
    team = models.CharField(max_length=5, unique=True, choices=TEAMS_CHOICES)
    latest_delivery_complete_at = models.DateTimeField(null=True, blank=True)


class OrderDeliveryInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    team_assigned = models.CharField(max_length=5, choices=TEAMS_CHOICES)
    delivery_start_at = models.DateTimeField()
    estimated_delivery_at = models.DateTimeField()
    actual_delivery_at = models.DateTimeField(null=True, blank=True)
    estimated_return_at = models.DateTimeField()
    actual_return_at = models.DateTimeField(null=True, blank=True)


def get_latest_order_no():
    current_date = dt.datetime.now(dt.timezone.utc).date()
    order_queryset = Order.objects.filter(
        timestamp__date=current_date
    )
    if order_queryset.exists():
        latest_order_no = order_queryset.aggregate( \
            Max('day_order_no'))['day_order_no__max']
        new_order_no = latest_order_no + 1
    else:
        new_order_no = 1

    order_number = current_date.strftime('%d%m%y') + '_' + str(new_order_no)

    return order_number, new_order_no
