# Generated by Django 4.0.4 on 2022-08-11 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]