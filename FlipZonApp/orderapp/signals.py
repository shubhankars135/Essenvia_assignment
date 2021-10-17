
import datetime as dt
import pytz

from .models import *

order_time = {
    'delivery_time' : {
        (0,5) : dt.timedelta(minutes=40),
        (5,10) : dt.timedelta(hours=1)
    },
    'return_time' : {
        (0,5) : dt.timedelta(minutes=20),
        (5,10) : dt.timedelta(minutes=40)     
    }
}


def create_delivery_info(sender, instance, created, **kwargs):
    if created:
        ist = pytz.timezone('Asia/Kolkata')
        current_tsp = dt.datetime.now().astimezone(ist)
        current_date = current_tsp.date()

        # fetch orders whose delivery is today
        delivery_queryset = OrderDeliveryInfo.objects.filter(
            delivery_start_at__date=current_date
        )

        if delivery_queryset.exists():
            delivery_team_queryset = DeliveryTeamInfo.objects.filter(
                latest_delivery_complete_at__lte=current_tsp)

            if delivery_team_queryset.exists(): # one or both team idle
                team_avialable = len(delivery_team_queryset)

                if team_avialable == 1: #one team idle - assign to other
                    idle_team = delivery_team_queryset[0].team
                    team_assigned = idle_team
                else: #both team idle - check which is idle for more time
                    latest_idle_team = delivery_team_queryset.latest(
                        'latest_delivery_complete_at').team

                    if latest_idle_team == 'a':
                        team_assigned = 'b' 
                    else:
                        team_assigned = 'a'

                delivery_start_at = instance.timestamp

            else: #both teams occupied
                latest_idle_team = DeliveryTeamInfo.objects.latest(
                        'latest_delivery_complete_at').team 

                if latest_idle_team == 'a':
                    team_assigned = 'b' 
                else:
                    team_assigned = 'a'
                    
                # delivery will after last order is complete
                delivery_start_at = DeliveryTeamInfo.objects.get(team=
                    team_assigned).latest_delivery_complete_at
        else:
            team_assigned = 'a' # any random
            delivery_start_at = instance.timestamp

        address_distance = instance.address_distance 
        if 10 >= address_distance > 5:
            key = (5,10)
        else:
            key = (0,5)

        estimated_delivery_at = delivery_start_at + order_time['delivery_time'][key] 
        estimated_return_at = estimated_delivery_at + order_time['return_time'][key]

        OrderDeliveryInfo(order=instance, team_assigned=team_assigned, 
            delivery_start_at=delivery_start_at, 
            estimated_delivery_at=estimated_delivery_at, 
            estimated_return_at=estimated_return_at).save()

        team_info_obj = DeliveryTeamInfo.objects.get(team=team_assigned)
        team_info_obj.latest_delivery_complete_at = estimated_return_at
        team_info_obj.save()


