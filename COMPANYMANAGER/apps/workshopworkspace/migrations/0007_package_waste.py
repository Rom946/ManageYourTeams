# Generated by Django 3.0 on 2020-07-20 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0055_wastecategory_available_for_workshop'),
        ('workshopworkspace', '0006_remove_workshopjob_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='waste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Waste'),
        ),
    ]
