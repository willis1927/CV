# Generated by Django 5.0.3 on 2024-04-15 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_bid_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
