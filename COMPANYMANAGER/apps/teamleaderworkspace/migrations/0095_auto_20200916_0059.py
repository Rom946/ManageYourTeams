# Generated by Django 3.0 on 2020-09-15 22:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamleaderworkspace', '0094_auto_20200915_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='SituationNCR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='qualityfeedback',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Car'),
        ),
        migrations.AddField(
            model_name='qualityfeedback',
            name='last_update',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='qualityfeedback',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Location'),
        ),
        migrations.AddField(
            model_name='qualityfeedback',
            name='part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Part'),
        ),
        migrations.AddField(
            model_name='qualityfeedback',
            name='train',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Train'),
        ),
        migrations.AlterField(
            model_name='qualityfeedback',
            name='team_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='qualityfeedback',
            name='tracking_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.TrackingCode'),
        ),
        migrations.AlterField(
            model_name='qualityfeedback',
            name='situation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.SituationNCR'),
        ),
    ]
