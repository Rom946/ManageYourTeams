# Generated by Django 3.0 on 2020-08-03 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_position'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamleaderworkspace', '0070_auto_20200803_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='teamleader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='job',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Car'),
        ),
        migrations.AlterField(
            model_name='job',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Part'),
        ),
        migrations.AlterField(
            model_name='job',
            name='team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='job',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Train'),
        ),
        migrations.AlterField(
            model_name='progressoncar',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Train'),
        ),
        migrations.AlterField(
            model_name='progressontrain',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Train'),
        ),
        migrations.AlterField(
            model_name='quantity',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Reference'),
        ),
        migrations.AlterField(
            model_name='referenceapplied',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Job'),
        ),
        migrations.AlterField(
            model_name='referenceapplied',
            name='reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Reference'),
        ),
        migrations.AlterField(
            model_name='referenceapplied',
            name='tech',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Tech'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Reference'),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Reference'),
        ),
        migrations.AlterField(
            model_name='tech',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='waste',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.WasteCategory'),
        ),
        migrations.AlterField(
            model_name='waste',
            name='job_waste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Job'),
        ),
        migrations.AlterField(
            model_name='waste',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Reference'),
        ),
        migrations.AlterField(
            model_name='waste',
            name='tech',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Tech'),
        ),
        migrations.AlterField(
            model_name='workbytech',
            name='team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workbytech',
            name='tech',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Tech'),
        ),
        migrations.AlterField(
            model_name='workdone',
            name='team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
