from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name', unique=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    is_listed = models.BooleanField(default=True, verbose_name='Is Listed')
    image = models.ImageField(upload_to='category_images/', null=True, blank=True, verbose_name='Image')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'