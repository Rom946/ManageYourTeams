# Generated by Django 3.0 on 2020-07-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0042_auto_20200705_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='car_type',
            field=models.CharField(choices=[('TC', 'TC'), ('M', 'M')], max_length=2),
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='possible_locations',
            field=models.ManyToManyField(to='teamleaderworkspace.Location'),
        ),
        migrations.AlterField(
            model_name='referenceapplied',
            name='locations',
            field=models.ManyToManyField(to='teamleaderworkspace.Location'),
        ),
        migrations.AlterField(
            model_name='referenceapplied',
            name='waste',
            field=models.ManyToManyField(to='teamleaderworkspace.Waste'),
        ),
    ]