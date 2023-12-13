import razorpay
from .models import Products,Cart,Orders
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .serializers import CartSerializer
from .serializers import ProductsSerializer, OrdersSerializer 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status,permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

@permission_classes([IsAuthenticated]) 
class ProductsViewSet(viewsets.ModelViewSet):
    def list(self, request):
        page_size = 2
        queryset = Products.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductsSerializer(
            result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    def perform_update(self, serializer):
        instance = serializer.save()
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request,Products_id):
    user = request.user
    #product_id = request.data.get('products_id')
    quantity = request.data.get('quantity', 1)

    try:
        product = Products.objects.get(id=Products_id)
    except Products.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if product.stock < quantity:
        return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    cart_item.quantity += quantity
    cart_item.save()

    product.stock -= quantity
    product.save()

    serializer = CartSerializer(cart_item)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart(request, cart_id):
    try:
        cart_item = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    # Restore stock
    product = cart_item.product
    product.stock += cart_item.quantity
    product.save()

    cart_item.delete()
    return Response({"message": "Cart item deleted and stock restored"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, cart_item_id, quantity):
    try:
        cart_item = Cart.objects.get(id=cart_item_id)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = CartSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            current_quantity = cart_item.quantity
            new_quantity = quantity

            if new_quantity == 0:
                cart_item.product.stock += current_quantity
                cart_item.product.save()
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            if new_quantity < current_quantity:
                quantity_diff = current_quantity - new_quantity

                if cart_item.product.stock < quantity_diff:
                    return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)

                cart_item.quantity = new_quantity
                cart_item.save()

                cart_item.product.stock += quantity_diff
                cart_item.product.save()

            elif new_quantity > current_quantity:
                quantity_diff = new_quantity - current_quantity

                if cart_item.product.stock < quantity_diff:
                    return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)

                cart_item.quantity = new_quantity
                cart_item.save()

                cart_item.product.stock -= quantity_diff
                cart_item.product.save()

            return Response(CartSerializer(cart_item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt  # Add this decorator to disable CSRF protection temporarily
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    user = request.user
    try:
        cart = Cart.objects.get(id=cart_id, user=user)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    # Calculate the total amount to be paid
    total_amount = cart.product.price * cart.quantity  # Assuming price is per unit

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    # Create a Razorpay order
    razorpay_order = client.order.create({
        'amount': int(total_amount * 100),  # Amount in paise (Indian currency)
        'currency': 'INR',
        'payment_capture': 1
    })

    # Create an entry in the Orders table with a pending status
    order = Orders.objects.create(
        user=user,
        product=cart.product, 
        total_amount=total_amount,
        status='pending',
        cart=cart,
        number_of_quantity=cart.quantity,
        individual_amount=cart.product.price,
        status_of_payment='Payment Successful'
    )

    # You can associate the Razorpay order ID with your order if needed
    order.razorpay_order_id = razorpay_order['id']
    order.save()

    return Response({'order_id': razorpay_order['id']}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_payment_success(request, cart_id):
    order_id = request.data.get('order_id')

    # Fetch the corresponding order from your database
    try:
        order = Orders.objects.get(razorpay_order_id=order_id)
    except Orders.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update the order status to 'paid' upon successful payment
    order.status = 'paid'
    order.save()

    try:
        order_item = Orders.objects.get(id=order_id)
    except Orders.DoesNotExist:
        return Response({"error": "order item not found"}, status=status.HTTP_404_NOT_FOUND)
    
    order_item.delete() 

    # Fetch the associated cart item using the 'cart' field of the order
    #order = Orders.objects.get(id=order_id) 
    #cart_item = order.cart

    #if cart_item:
        #cart_item.delete()
    #else:
        #return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    # You can also perform other actions here, such as sending order confirmation emails

    return Response({"message": "Payment successful", "order_id": order.id}, status=status.HTTP_200_OK)


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_order(request):
    user = request.user 
    cart_items = Orders.objects.filter(user=user)
    serializer = OrdersSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request):
    user = request.user
    order_items = Orders.objects.filter(user=user)

    order_items.delete()
    return Response({"message": "deleted all orders"}, status=status.HTTP_204_NO_CONTENT)
