from rest_framework import serializers
from api.models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vendor
        fields='__all__'
        read_only_fields=['id','vendor_code']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= PurchaseOrder
        fields='__all__'
        read_only_fields=['id','po_number']

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model= HistoricalPerformance
        fields='__all__'