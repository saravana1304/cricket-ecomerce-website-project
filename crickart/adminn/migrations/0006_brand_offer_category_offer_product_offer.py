# Generated by Django 5.0.4 on 2024-05-20 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminn', '0005_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='offer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Offer'),
        ),
        migrations.AddField(
            model_name='category',
            name='offer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Offer'),
        ),
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Offer'),
        ),
    ]