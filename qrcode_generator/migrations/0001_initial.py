# Generated by Django 4.0.4 on 2022-08-08 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QrCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('image', models.ImageField(blank=True, upload_to='qrcode')),
            ],
        ),
    ]
