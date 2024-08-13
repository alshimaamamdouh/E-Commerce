from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CartViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

cart_list = CartViewSet.as_view({'get': 'list_cart'})
cart_add = CartViewSet.as_view({'post': 'add_to_cart'})
cart_update = CartViewSet.as_view({'put': 'update_cart'})
cart_remove = CartViewSet.as_view({'delete': 'remove_from_cart'})

urlpatterns = [
    path('', include(router.urls)),
    path('cart/<int:user_id>/', cart_list),
    path('cart/<int:user_id>/add/', cart_add),
    path('cart/<int:user_id>/update/', cart_update),
    path('cart/<int:user_id>/remove/<int:product_id>/', cart_remove),
]
