
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Product, CartItem, Test_coll
from .serializers import ProductSerializer, CartItemSerializer
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader




def index(request):

   #template = loader.get_template('backend/index.html')
   #return HttpResponse(template.render())
   #data = {'name':'alshimaa', 'job':'engineer'}
   #data = {'name':'Mobile', 'price':'123LE', 'seller_name':'global company'}
   #tt =  Test_coll(name='Mobile')
   #tt.save()
   return render(request, 'backend/index.html') 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def list_cart(self, request, user_id):
        cart_items = CartItem.objects.filter(user_id=user_id)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request, user_id):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
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
        cart_item = CartItem.objects.get(user_id=user_id, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def remove_from_cart(self, request, user_id, product_id):
        cart_item = CartItem.objects.get(user_id=user_id, product_id=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

