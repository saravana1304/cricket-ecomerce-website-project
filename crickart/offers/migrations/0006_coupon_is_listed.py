# Generated by Django 5.0.4 on 2024-05-11 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0005_alter_coupon_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]