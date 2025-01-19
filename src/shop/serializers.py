from rest_framework import serializers
from .models import Product, Order, Category, ProductImage, ProductPriceHistory
from django.utils.timezone import now
from django.db import transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Explicitly allow `id`

    class Meta:
        model = ProductImage
        # excluding product from ProductImageSerializer, allow the parent ProductSerializer to handle associating images with the correct product
        fields = ['id', 'filename', 'image', 'is_primary']

class ProductSerializer(serializers.ModelSerializer):
    """
    product serializer
    todo If you want to fetch the latest price history or history for a specific time range, you can use Django ORM queries on ProductPriceHistory.
    """
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                # Extract images from validated data
                images_data = validated_data.pop('images', [])

                # create product object
                product = Product.objects.create(**validated_data)

                # create product image objects for the product
                for image in images_data:
                    ProductImage.objects.create(product=product, **image)

                # create a price history record
                ProductPriceHistory.objects.create(
                    product = product,
                    price = product.current_price
                )
        except Exception as e:
            raise e
            # raise serializers.ValidationError({"detail": "Failed to create product object."}) from e
        return product

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                # update or create product images if it has
                images_data = validated_data.pop('images', [])
                for image_data in images_data:
                    image_id = image_data.get('id', None)
                    if image_id:
                        # update existing image
                        product_image = ProductImage.objects.get(id=image_id, product=instance)
                        for attr, value in image_data.items():
                            setattr(product_image, attr, value)
                        product_image.save()
                    else:
                        # create new product image
                        ProductImage.objects.create(product=instance, **image_data)

                # Check if the price is being updated
                new_price = validated_data.get('current_price')
                if new_price and new_price != instance.current_price:
                    # Update the end_date of the most recent price history record
                    last_price_history = instance.price_histories.filter(end_date__isnull=True).last()
                    if last_price_history:
                        last_price_history.end_date = now()
                        last_price_history.save()

                    # Create a new ProductPriceHistory record for the new price
                    ProductPriceHistory.objects.create(
                        product=instance,
                        price=new_price
                    )

                # update product
                instance = super().update(instance, validated_data)
        except Exception as e:
            raise e
        return instance

class ProductPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPriceHistory
        fields = ['id', 'price', 'start_date', 'end_date']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
