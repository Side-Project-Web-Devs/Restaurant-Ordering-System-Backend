# Generated by Django 4.0.4 on 2022-08-27 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0016_add_to_cart_x'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='add_to_cart',
            name='x',
        ),
    ]
