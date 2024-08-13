from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from .models import Product, CartItem, Category, Order, OrderItem, Review
from .serializers import ProductSerializer, CartItemSerializer, CategorySerializer, OrderSerializer, ReviewSerializer, UserSerializer


def index(request):
    return render(request, 'backend/index.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(UserViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def list_cart(self, request, user_id):
        cart_items = CartItem.objects.filter(user_id=user_id).select_related('product')
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request, user_id):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        user = get_object_or_404(User, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'])
    def update_cart(self, request, user_id):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        cart_item = get_object_or_404(CartItem, user_id=user_id, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def remove_from_cart(self, request, user_id, product_id):
        cart_item = get_object_or_404(CartItem, user_id=user_id, product_id=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def create_order(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        order = Order.objects.create(user=user, total_price=0)
        
        cart_items = CartItem.objects.filter(user=user)
        total_price = 0
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            total_price += item.product.price * item.quantity
        order.total_price = total_price
        order.save()

        cart_items.delete()  # Clear the cart after creating the order

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
