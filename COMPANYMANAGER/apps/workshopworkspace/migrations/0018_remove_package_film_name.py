# Generated by Django 3.0 on 2020-07-29 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshopworkspace', '0017_auto_20200729_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='film_name',
        ),
    ]
