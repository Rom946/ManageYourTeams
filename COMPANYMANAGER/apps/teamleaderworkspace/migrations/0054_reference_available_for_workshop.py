# Generated by Django 3.0 on 2020-07-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0053_waste_job_waste'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='available_for_workshop',
            field=models.BooleanField(default=False),
        ),
    ]
