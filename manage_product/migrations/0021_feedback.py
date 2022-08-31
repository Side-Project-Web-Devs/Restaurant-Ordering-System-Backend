# Generated by Django 4.0.4 on 2022-08-29 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_customer_user_customer_name'),
        ('manage_product', '0020_alter_manage_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(max_length=1000, null=True)),
                ('reply', models.TextField(max_length=1000, null=True)),
                ('cus', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
                ('pro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_product.manage_product')),
            ],
        ),
    ]