# Generated by Django 3.0 on 2020-06-24 23:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamleaderworkspace', '0020_auto_20200625_0136'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PartLinks',
            new_name='Job',
        ),
    ]