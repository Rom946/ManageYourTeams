# Generated by Django 3.0 on 2020-09-15 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0091_auto_20200915_2051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workdone',
            options={'ordering': ['id']},
        ),
    ]
