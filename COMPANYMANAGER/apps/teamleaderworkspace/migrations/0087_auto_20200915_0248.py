# Generated by Django 3.0 on 2020-09-15 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0086_waste_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waste',
            name='location',
            field=models.ManyToManyField(blank=True, to='teamleaderworkspace.Location'),
        ),
    ]