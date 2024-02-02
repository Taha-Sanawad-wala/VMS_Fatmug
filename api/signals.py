from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import PurchaseOrder,Vendor, HistoricalPerformance
from django.db.models import F, ExpressionWrapper, fields, Avg
from datetime import datetime
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    # Your existing code for updating performance metrics goes here
        print(sender, instance.vendor, created)
        vendor = Vendor.objects.get(vendor_code=instance.vendor)
        # On-Time Delivery Rate:
        #need more insight on how to calculate

        # Quality Rating:
        quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor).aggregate(Avg('quality_rating'))['quality_rating__avg']
        
        # Average Response Time:between issue_date and acknowledgment_date
        average_time_difference = PurchaseOrder.objects.filter(vendor=vendor).annotate(
        time_difference=ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=fields.DurationField()
            )
            ).aggregate(avg_time_difference=Avg('time_difference'))['avg_time_difference'].total_seconds()
        

        # Fulfilment Rate:
        try:
            fulfilment_rate=PurchaseOrder.objects.filter(vendor=vendor).filter(status='completed').count()/PurchaseOrder.objects.filter(vendor=vendor).count()
        except:
            fulfilment_rate=0
        id=HistoricalPerformance.objects.filter(vendor=vendor).values_list('id')
        if id:   
            historical_performance= HistoricalPerformance(
            id=id[0][0],
            vendor=vendor,
            date=datetime.now(),
            on_time_delivery_rate= 00,
            quality_rating_avg=quality_rating_avg,
            average_response_time= average_time_difference,
            fulfillment_rate= fulfilment_rate
            )   
            historical_performance.save()  
            vendor.on_time_delivery_rate=00
            vendor.quality_rating_avg=quality_rating_avg
            vendor.average_response_time=average_time_difference
            vendor.fulfillment_rate=fulfilment_rate
            vendor.save()          
            print({"msg":f"Performance update for vendor:{vendor}"})
        else:
            historical_performance= HistoricalPerformance(
            vendor=vendor,
            date=datetime.now(),
            on_time_delivery_rate= 00,
            quality_rating_avg=quality_rating_avg,
            average_response_time= average_time_difference,
            fulfillment_rate= fulfilment_rate
            )   
            historical_performance.save()  
            vendor.on_time_delivery_rate=00
            vendor.quality_rating_avg=quality_rating_avg
            vendor.average_response_time=average_time_difference
            vendor.fulfillment_rate=fulfilment_rate
            vendor.save()             
            print({"msg":f"Performance created for vendor:{vendor}"})