# Generated by Django 5.0.3 on 2024-03-23 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_remove_listing_endtime_listing_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='reserve',
        ),
    ]
