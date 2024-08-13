from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, 
    CartViewSet, 
    UserViewSet, 
    CategoryViewSet, 
    OrderViewSet, 
    ReviewViewSet, 
    index
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'users', UserViewSet, basename='user')

cart_list = CartViewSet.as_view({'get': 'list_cart'})
cart_add = CartViewSet.as_view({'post': 'add_to_cart'})
cart_update = CartViewSet.as_view({'put': 'update_cart'})
cart_remove = CartViewSet.as_view({'delete': 'remove_from_cart'})

urlpatterns = [
    path('', include(router.urls)),  # Automatically includes all router URLs
    path('index/', index, name='index'),
    path('cart/<int:user_id>/', cart_list, name='cart-list'),
    path('cart/<int:user_id>/add/', cart_add, name='cart-add'),
    path('cart/<int:user_id>/update/', cart_update, name='cart-update'),
    path('cart/<int:user_id>/remove/<int:product_id>/', cart_remove, name='cart-remove'),
    
    # Specific actions for products and reviews
    path('products/add/', ProductViewSet.as_view({'post': 'create'}), name='product-create'),
    
    
    # User management
    path('users/<int:pk>/update/', UserViewSet.as_view({'put': 'update'}), name='user-update'),
    path('users/<int:pk>/delete/', UserViewSet.as_view({'delete': 'destroy'}), name='user-delete'),
    
    # Review management
    path('reviews/add/', ReviewViewSet.as_view({'post': 'create'}), name='review-create'),
    path('reviews/<int:pk>/update/', ReviewViewSet.as_view({'put': 'update'}), name='review-update'),
    path('reviews/<int:pk>/delete/', ReviewViewSet.as_view({'delete': 'destroy'}), name='review-delete'),
    
    # Category management
    path('categories/<int:pk>/update/', CategoryViewSet.as_view({'put': 'update'}), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryViewSet.as_view({'delete': 'destroy'}), name='category-delete'),
]
