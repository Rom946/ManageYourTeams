# Generated by Django 3.0 on 2020-08-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0080_quantity_exempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quantity',
            name='car_type',
        ),
        migrations.RemoveField(
            model_name='quantity',
            name='exempt',
        ),
        migrations.RemoveField(
            model_name='quantity',
            name='qty_needed',
        ),
        migrations.AddField(
            model_name='quantity',
            name='M1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quantity',
            name='M2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quantity',
            name='M3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quantity',
            name='M4',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quantity',
            name='TC1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quantity',
            name='TC2',
            field=models.IntegerField(default=0),
        ),
    ]
