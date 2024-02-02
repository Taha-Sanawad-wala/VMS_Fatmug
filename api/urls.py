from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from api.views import vendor, purchase_order, performance, acknowledge_purchase_order, authenticate_user
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView




urlpatterns = [
path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # Spectacular schema endpoint
path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # Spectacular Swagger UI endpoint
path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # Spectacular ReDoc endpoint
# Your other API endpoints
path('authenticate/', authenticate_user),
path('vendors/', vendor, name='vendor_display'),
path('vendors/<int:pk>', vendor, name='vendor_edit'),
path('purchase_order/', purchase_order, name='purchase_order_display'),
path('purchase_order/<int:pk>', purchase_order, name='purchase_order_edit'),
path('vendors/<int:pk>/performance/', performance, name='performance_metrics'),
path('purchase_orders/<int:pk>/acknowledge/', acknowledge_purchase_order, name='purchase_order_acknowledge'),

]