# Generated by Django 3.0 on 2020-07-22 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshopworkspace', '0014_package_had_stock_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layoutplan',
            name='nb_of_ref_possible',
            field=models.IntegerField(default=1),
        ),
    ]
