from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    ProductsViewSet, 
    UserViewSet, 
    CategoryViewSet, 
    CartViewSet, 
    OrderViewSet, 
    ReviewViewSet
)

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'users', UserViewSet, basename='user')

# Cart view actions
cart_list = CartViewSet.as_view({'get': 'list_cart'})
cart_add = CartViewSet.as_view({'post': 'add_to_cart'})
cart_update = CartViewSet.as_view({'put': 'update_cart'})
cart_remove = CartViewSet.as_view({'delete': 'remove_from_cart'})

# Product view actions
product_add = ProductsViewSet.as_view({'post': 'create_product'})
product_get = ProductsViewSet.as_view({'get': 'list_products'})
product_update = ProductsViewSet.as_view({'put': 'update_product'})
product_del = ProductsViewSet.as_view({'delete': 'delete_product'})

# category view actions
category_add = CategoryViewSet.as_view({'post': 'create_category'})
category_get = CategoryViewSet.as_view({'get': 'list_category'})
category_update = CategoryViewSet.as_view({'put': 'update_category'})
category_del = CategoryViewSet.as_view({'delete': 'delete_category'})

urlpatterns = [
    path('', include(router.urls)), 
    
    # Cart
    path('cart/<int:user_id>/', cart_list, name='cart-list'),
    path('cart/add/', cart_add, name='cart-add'),
    path('cart/<int:user_id>/update/', cart_update, name='cart-update'),
    path('cart/<int:user_id>/remove/<int:product_id>/', cart_remove, name='cart-remove'),
    
    # Product 
    path('products_add/', product_add, name='product_add'),
    path('products_get/', product_get, name='product_get'),
    path('products/<int:pk>/update/', product_update, name='product_update'),
    path('products/<int:pk>/delete/', product_del, name='product_delete'),

    # Category
    path('categories_add/', category_add, name='category_add'),
    path('categories_get/', category_get, name='category_get'),
    path('categories/<int:pk>/update/', category_update, name='category_update'),
    path('categories/<int:pk>/delete/', category_del, name='category_delete'),

    # User 
    path('users/<int:pk>/update/', UserViewSet.as_view({'put': 'update'}), name='user_update'),
    path('users/<int:pk>/delete/', UserViewSet.as_view({'delete': 'destroy'}), name='user_delete'),
    
    # Review 
    path('reviews/add/', ReviewViewSet.as_view({'post': 'create'}), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewViewSet.as_view({'put': 'update'}), name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewViewSet.as_view({'delete': 'destroy'}), name='review_delete'),
]
