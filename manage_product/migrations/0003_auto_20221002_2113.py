# Generated by Django 2.1.15 on 2022-10-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0002_add_to_cart_if_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_to_cart',
            name='dine_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='add_to_cart',
            name='take_out',
            field=models.BooleanField(default=False),
        ),
    ]