# Generated by Django 3.1.4 on 2020-12-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listings_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]