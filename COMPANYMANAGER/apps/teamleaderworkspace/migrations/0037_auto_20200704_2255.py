# Generated by Django 3.0 on 2020-07-04 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0036_auto_20200704_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referenceapplied',
            name='date_work',
        ),
        migrations.RemoveField(
            model_name='referenceapplied',
            name='job',
        ),
        migrations.RemoveField(
            model_name='referenceapplied',
            name='locations',
        ),
        migrations.RemoveField(
            model_name='referenceapplied',
            name='waste',
        ),
    ]