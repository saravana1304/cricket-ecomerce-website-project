from django.contrib.auth.models import User
from django.db import models
from adminn.models import Product
from userapp1.models import UserProfile


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} ({self.user.username})"
    
    def total_price(self):
        return self.quantity * self.selling_price



class Address(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    phone_number = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=20)

