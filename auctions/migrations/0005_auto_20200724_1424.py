# Generated by Django 3.0.8 on 2020-07-24 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_listing_startdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='details',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='images',
        ),
    ]
