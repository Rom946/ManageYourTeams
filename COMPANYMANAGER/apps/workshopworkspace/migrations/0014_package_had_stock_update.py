# Generated by Django 3.0 on 2020-07-22 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshopworkspace', '0013_auto_20200722_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='had_stock_update',
            field=models.BooleanField(default=False),
        ),
    ]
