# Generated by Django 3.0 on 2020-06-13 00:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamleaderworkspace', '0015_auto_20200612_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliedby',
            name='team_leader',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partlinks',
            name='team_leader',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamlinks',
            name='team_leader',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donetoday',
            name='team_leader',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
