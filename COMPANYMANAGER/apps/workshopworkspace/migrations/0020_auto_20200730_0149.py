# Generated by Django 3.0 on 2020-07-29 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshopworkspace', '0019_auto_20200729_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockfilm',
            name='qty',
            field=models.IntegerField(default=0),
        ),
    ]
