# Generated by Django 3.0 on 2020-06-09 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0006_auto_20200529_0421'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Car'),
        ),
    ]
