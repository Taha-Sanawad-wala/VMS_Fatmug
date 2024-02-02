from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Vendor, PurchaseOrder, HistoricalPerformance
from api.serializers import VendorSerializer,PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework import status
from django.db.models import F, ExpressionWrapper, fields, Avg
from datetime import datetime
from django.urls import reverse
from django.http import JsonResponse
from api.utils import create_token_for_user
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
# Create your views here.

@api_view(['GET'])
def authenticate_user(request):
    username = "tahas" 
    token = create_token_for_user(username)
    return JsonResponse({'message': 'Authenticated with token!', 'token': str(token)})


# api starts here

@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor(request, pk=None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            vendor = Vendor.objects.get(id=id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        queryset= Vendor.objects.all()
        serializer=VendorSerializer(queryset,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor=Vendor(**serializer.data)
            vendor.save()
            return Response({'msg': 'Vendor Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        id = pk
        vendor = Vendor.objects.get(id=id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Vendor Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        id = pk
        vendor = Vendor.objects.get(id=id)
        vendor.delete()
        return Response({'msg': 'Vendor Deleted'})



@api_view(['GET','POST','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order(request, pk=None):
    if request.method == 'GET':
        id = pk
        if id is not None:
            purchase_order = PurchaseOrder.objects.get(id=id)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        queryset= PurchaseOrder.objects.all()
        serializer=PurchaseOrderSerializer(queryset,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            vendor_data = serializer.validated_data.get('vendor')
            serializer.validated_data.pop('vendor')
            vendor_instance = Vendor.objects.get(vendor_code=vendor_data)
            purchase_order=PurchaseOrder(vendor=vendor_instance,**serializer.validated_data)
            purchase_order.save()
            return Response({'msg': 'Purchase Order Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        id = pk
        purchase_order = PurchaseOrder.objects.get(id=id)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Purchase Order Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        # id = request.data.get('id')
        id = pk
        purchase_order = PurchaseOrder.objects.get(id=id)
        purchase_order.delete()
        return Response({'msg': 'Purchase Order Deleted'})

    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, pk=None):
    purchase_order = PurchaseOrder.objects.get(id=pk)
    if PurchaseOrder.objects.filter(id=pk).filter(acknowledgment_date__isnull=True):
        purchase_order.acknowledgment_date=datetime.now()
        purchase_order.save()
        return Response({'msg':'Purchase order Acknowledge'},)
    else:
        return Response({"msg":"Purchase Order Already Acknowledge"})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def performance(request,pk=None):
    if request.method=='GET':
        performance_metric=HistoricalPerformance.objects.filter(vendor=pk).values()
        return Response({performance_metric})
    
    