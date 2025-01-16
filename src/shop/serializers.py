from rest_framework import serializers
from .models import Product, Order, Category, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        # fields = ['id', 'image', 'alt_text']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        # create product object
        product = Product.objects.create(**validated_data)

        if 'images' in validated_data:
            # get images data
            images_data = validated_data.pop('images')
            # create product image objects for the product
            for image in images_data:
                ProductImage.objects.create(product=product, **image)

        return product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
