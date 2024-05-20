from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal



# Create your models here.

# models for Category
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name', unique=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    is_listed = models.BooleanField(default=True, verbose_name='Is Listed')
    image = models.ImageField(upload_to='category_images/', null=True, blank=True, verbose_name='Image')
    offer = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Offer')  # Added offer field

    class Meta:
        verbose_name_plural = 'Categories'

# models for Brand
class Brand(models.Model):
    name = models.CharField(max_length=50)
    is_listed = models.BooleanField(default=True) 
    offer = models.DecimalField(max_digits=5, decimal_places=2, default=0) 


# models for Product
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    is_listed = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name='Image 1')
    image2 = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name='Image 2')
    image3 = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name='Image 3')
    stock = models.PositiveIntegerField(null=False, default=0)  
    landing_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    offer = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Offer')

    def clean(self):
        # Add any custom validation logic here
        if self.selling_price is not None and self.selling_price < self.landing_price:
            raise ValidationError("Selling price cannot be less than landing price")
        
    # getting highest offer 
    def get_highest_offer(self):
        return max(self.category.offer, self.brand.offer, self.offer)
    
    # calculating a discount price 
    def get_discounted_price(self):
        highest_offer = self.get_highest_offer()
        discount = (highest_offer / Decimal(100)) * self.selling_price
        discounted_price = self.selling_price - discount
        return int (discounted_price)
    
