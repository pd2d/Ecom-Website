from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Define choices for stock status
STOCK_CHOICES = (
    ('in_stock', 'In Stock'),
    ('out_of_stock', 'Out of Stock'),
    ('low_stock', 'Low Stock'),
)

SIZE_CHOICES = (
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large'),
    ('extra_large', 'Extra_Large'),
)

class Company(models.Model):
    name = models.CharField(max_length=100)

class Products(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)
    discription = models.TextField()

    def stock_status(self):
        if self.stock == 0:
            return 'out_of_stock'
        elif self.stock < 10:
            return 'stock_out_soon'
        else:
            return 'in_stock'
    

class Images(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    images = models.ImageField(upload_to='product_images/')

class category(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    number_of_quantity = models.PositiveIntegerField(default=0)
    individual_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status_of_payment = models.CharField(max_length=20, blank=True) 
    status = models.CharField(max_length=20, default='pending')  
    created_at = models.DateTimeField(default=timezone.now())



    
class payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    amount=models.CharField(max_length=50)
    date=models.CharField(max_length=50)

