# Generated by Django 3.0 on 2020-06-24 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0019_auto_20200625_0021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appliedby',
            old_name='date_worked',
            new_name='date_work',
        ),
        migrations.RenameField(
            model_name='workbytech',
            old_name='work_date',
            new_name='date_work',
        ),
    ]