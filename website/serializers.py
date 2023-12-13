from rest_framework import serializers
from .models import Products,Cart,Images, User, Orders

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = ('id', 'name', 'company', 'size', 'price',
                  'stock', 'discription', 'images', 'stock_status')
            
    def get_images(self, instance):
        image = Images.objects.filter(
            product=instance.id).values_list('images', flat=True)
        return image

    
class CartSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    total_price = serializers.SerializerMethodField() 
    class Meta:
        model = Cart
        fields = ('id', 'quantity', 'user', 'product', 'total_price', 'created_at')
        
    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
    
    
    
    
