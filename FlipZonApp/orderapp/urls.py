from django.urls import path, include

from . import views
from . import viewsets

from rest_framework.routers import DefaultRouter

 
router_v1 = DefaultRouter()
router_v1.register('orders', viewsets.OrderViewSet)
router_v1.register('item_inventory', viewsets.ItemInventoryViewSet)
router_v1.register('order_info', viewsets.OrderDeliveryInfoViewSet)


urlpatterns = [
    path('get_order_no', views.get_order_no, name='get_order_no'),
    path('fill_db', views.fill_inventory, name='fill_inventory'),
    path('generate_day_report', views.generate_day_report, name='generate_day_report'),

    path('v1/', include(router_v1.urls)),
]


