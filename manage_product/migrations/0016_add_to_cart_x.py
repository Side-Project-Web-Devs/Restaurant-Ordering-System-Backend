# Generated by Django 4.0.4 on 2022-08-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0015_alter_manage_product_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_to_cart',
            name='x',
            field=models.IntegerField(default=0),
        ),
    ]
