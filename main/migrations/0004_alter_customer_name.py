# Generated by Django 4.0.4 on 2022-08-10 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_customer_orders_remove_customer_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]