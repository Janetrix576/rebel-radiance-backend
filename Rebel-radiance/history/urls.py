from django.urls import path, include  
from rest_framework.routers import DefaultRouter
from . import views 

router = DefaultRouter()

router.register(r'products', views.ProductViewSet, basename='product') 
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'order-history', views.OrderHistoryViewSet, basename='orderhistory')
router.register(r'product-changelog', views.ProductChangeLogViewSet, basename='productchangelog')

urlpatterns = router.urls 