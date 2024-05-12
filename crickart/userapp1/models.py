from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits')])
    place = models.CharField(max_length=255)
    address = models.TextField(null=True)
    pincode = models.IntegerField(null=True, blank=True, default=None)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username
