from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, CartItem, Category, Order, OrderItem, Review
from djongo import models as djongo_models
from rest_framework.exceptions import ValidationError

# Custom serializer for ObjectId
class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, djongo_models.ObjectId):
            return str(value)
        raise ValidationError("Value is not of type ObjectId")

    def to_internal_value(self, data):
        try:
            return djongo_models.ObjectId(data)
        except Exception as e:
            raise ValidationError(f"Invalid ObjectId: {e}")

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    id = ObjectIdField()

    class Meta:
        model = Category
        fields = '__all__'

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = ObjectIdField(source='category', write_only=True)

    class Meta:
        model = Product
        fields = '__all__'

# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = ObjectIdField(source='product', write_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'

# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = ObjectIdField(source='product', write_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = ObjectIdField(source='product', write_only=True)

    class Meta:
        model = Review
        fields = '__all__'
