# Generated by Django 5.0.3 on 2024-03-23 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listing_imageurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='endTime',
        ),
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default='True'),
        ),
    ]
