# Generated by Django 5.0.4 on 2024-05-11 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_coupon_is_listed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='status',
        ),
    ]