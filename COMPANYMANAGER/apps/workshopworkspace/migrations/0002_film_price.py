# Generated by Django 3.0 on 2020-07-20 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshopworkspace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]