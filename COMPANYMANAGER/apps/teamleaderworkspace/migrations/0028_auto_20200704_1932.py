# Generated by Django 3.0 on 2020-07-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0027_auto_20200703_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waste',
            name='qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]