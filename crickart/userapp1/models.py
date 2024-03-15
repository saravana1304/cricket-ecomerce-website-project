from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
import secrets


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits')])
    place = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
