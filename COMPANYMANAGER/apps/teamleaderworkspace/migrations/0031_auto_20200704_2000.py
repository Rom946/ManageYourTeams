# Generated by Django 3.0 on 2020-07-04 18:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0030_auto_20200704_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referenceapplied',
            name='qty',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
