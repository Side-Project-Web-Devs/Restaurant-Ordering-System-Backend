# Generated by Django 4.0.4 on 2022-08-11 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_customer_user_customer_name'),
        ('manage_product', '0009_remove_add_to_cart_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_to_cart',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.customer'),
        ),
    ]
