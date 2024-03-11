from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('block', 'Block'),
        ('unblock', 'Unblock'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.user.username
