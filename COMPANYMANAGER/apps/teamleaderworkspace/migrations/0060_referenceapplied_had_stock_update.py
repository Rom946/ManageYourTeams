# Generated by Django 3.0 on 2020-07-27 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0059_auto_20200721_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='referenceapplied',
            name='had_stock_update',
            field=models.BooleanField(default=False),
        ),
    ]