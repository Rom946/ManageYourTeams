# Generated by Django 3.0 on 2020-07-20 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_position'),
        ('teamleaderworkspace', '0055_wastecategory_available_for_workshop'),
    ]

    operations = [
        migrations.AddField(
            model_name='waste',
            name='workshop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
    ]
