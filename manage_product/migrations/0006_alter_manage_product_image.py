# Generated by Django 4.0.4 on 2022-08-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0005_alter_manage_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manage_product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_image/'),
        ),
    ]
