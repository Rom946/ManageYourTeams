# Generated by Django 3.0 on 2020-09-16 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0104_auto_20200916_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quality',
            name='qty_applied',
        ),
    ]