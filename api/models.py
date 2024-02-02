from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True,editable=False)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            super().save(*args, **kwargs)
            prefix = "VN-"
            self.vendor_code = f"{prefix}{self.id}"
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.vendor_code
    

class PurchaseOrder(models.Model):
    status_options=(('pending','pending'),
    ('completed','completed'),
    ('canceled','canceled'))
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50, unique=True,editable=False)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(default=[{"name":'___', "color":'___'}])
    quantity = models.IntegerField()
    status = models.CharField(max_length=50,choices=status_options)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.po_number:
            super().save(*args, **kwargs)
            prefix = "PO-"
            self.po_number = f"{prefix}{self.id}"
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()