# Generated by Django 3.0 on 2020-08-03 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_position'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamleaderworkspace', '0073_auto_20200803_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QualityFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('situation', models.CharField(max_length=200)),
                ('replacement', models.BooleanField(default=False)),
                ('ncr_number', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('files', models.FileField(blank=True, null=True, upload_to='')),
                ('date_record', models.DateField()),
                ('inspector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
                ('team_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tracking_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.TrackingCode')),
            ],
        ),
    ]
