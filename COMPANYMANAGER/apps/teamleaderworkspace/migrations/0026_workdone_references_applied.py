# Generated by Django 3.0 on 2020-07-01 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0025_referenceapplied'),
    ]

    operations = [
        migrations.AddField(
            model_name='workdone',
            name='references_applied',
            field=models.ManyToManyField(to='teamleaderworkspace.ReferenceApplied'),
        ),
    ]
