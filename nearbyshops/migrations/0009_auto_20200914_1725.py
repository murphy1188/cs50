# Generated by Django 3.1 on 2020-09-14 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nearbyshops', '0008_auto_20200914_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='john',
            name='street_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
