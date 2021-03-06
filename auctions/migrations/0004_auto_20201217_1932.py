# Generated by Django 3.1.4 on 2020-12-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listings_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='listings',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='listings',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
