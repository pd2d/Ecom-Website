from . import views
from .views import ProductsViewSet
from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import add_to_cart, view_cart, delete_cart, update_cart_item, initiate_payment, view_order, delete_order

router = DefaultRouter()
router.register('products', ProductsViewSet,
                basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('view_cart/', view_cart, name='view_cart'),
    path('view_order/', view_order, name='view_order'),
    path('add_cart/<int:Products_id>/', add_to_cart, name='add_cart'),
    path('delete_cart/<int:cart_id>/', delete_cart, name='delete_cart'),
    path('delete_orders/', delete_order, name='delete_order'),
    path('buy/<int:cart_id>/', initiate_payment, name='initiate-payment'),
    path('update_cart/<int:cart_item_id>/<int:quantity>/', update_cart_item, name='update-cart-item'),
]
