# Generated by Django 4.0.4 on 2022-08-11 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0010_add_to_cart_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_to_cart',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_product.manage_product'),
        ),
    ]
