# Generated by Django 3.0 on 2020-07-31 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0064_auto_20200731_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressoncar',
            name='progress_on_part',
            field=models.ManyToManyField(to='teamleaderworkspace.ProgressOnPart'),
        ),
    ]
