# Generated by Django 3.0 on 2020-08-03 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0071_auto_20200803_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='waste',
            name='date_waste',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
