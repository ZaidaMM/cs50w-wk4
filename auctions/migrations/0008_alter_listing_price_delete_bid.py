# Generated by Django 4.2 on 2023-04-26 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_bid_bid_alter_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(),
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
    ]
