from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, TagViewSet

def api_root(request):
    return JsonResponse({
        "message": "Welcome to the Rebel Radiance API",
        "endpoints": {
            "products": "/api/products/",
            "categories": "/api/categories/",
            "tags": "/api/tags/"
        }
    })

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', api_root),
]
