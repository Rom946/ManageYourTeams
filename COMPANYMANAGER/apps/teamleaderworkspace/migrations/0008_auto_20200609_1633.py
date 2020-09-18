# Generated by Django 3.0 on 2020-06-09 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0007_part_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='car',
        ),
        migrations.AddField(
            model_name='part',
            name='car',
            field=models.ManyToManyField(to='teamleaderworkspace.Car'),
        ),
    ]
