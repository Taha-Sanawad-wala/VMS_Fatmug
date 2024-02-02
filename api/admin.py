from django.contrib import admin
from api.models import Vendor,PurchaseOrder,HistoricalPerformance


class VendorAdmin(admin.ModelAdmin):
    list_display=['id','name','contact_details','address','vendor_code','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']

class PerchaseOrderAdmin(admin.ModelAdmin):
    list_display=['id','vendor','po_number','order_date','delivery_date','items','quantity','status','quality_rating','issue_date','acknowledgment_date']

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display=['id','vendor','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']
 

admin.site.register(Vendor,VendorAdmin)
admin.site.register(PurchaseOrder,PerchaseOrderAdmin)
admin.site.register(HistoricalPerformance,HistoricalPerformanceAdmin)