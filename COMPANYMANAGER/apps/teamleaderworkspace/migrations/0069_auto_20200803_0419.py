# Generated by Django 3.0 on 2020-08-03 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0068_auto_20200803_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressoncar',
            name='last_update',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='progressonpart',
            name='last_update',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='progressontrain',
            name='last_update',
            field=models.DateField(auto_now=True),
        ),
    ]
