from django.contrib.auth.models import User
from django.db import models
from adminn.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} ({self.user.username})"

