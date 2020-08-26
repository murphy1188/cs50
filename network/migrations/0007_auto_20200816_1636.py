# Generated by Django 3.0.8 on 2020-08-16 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20200816_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='commenter',
        ),
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='postcomments', to='network.Comment'),
        ),
    ]
