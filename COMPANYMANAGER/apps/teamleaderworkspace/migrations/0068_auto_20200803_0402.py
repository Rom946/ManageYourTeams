# Generated by Django 3.0 on 2020-08-03 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0067_auto_20200731_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='qty_needed',
            field=models.IntegerField(default=0),
        ),
    ]