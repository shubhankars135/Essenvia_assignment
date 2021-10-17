from django.apps import AppConfig
from django.db.models.signals import post_save



class OrderappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orderapp'

    def ready(self):
        from .signals import create_delivery_info
        from .models import Order
        
        post_save.connect(create_delivery_info, sender=Order)
