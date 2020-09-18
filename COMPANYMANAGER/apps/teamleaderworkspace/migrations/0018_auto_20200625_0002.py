# Generated by Django 3.0 on 2020-06-24 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamleaderworkspace', '0017_auto_20200617_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkByTech',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField(auto_now=True)),
                ('team_leader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('tech', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Tech')),
                ('work', models.ManyToManyField(to='teamleaderworkspace.PartLinks')),
            ],
            options={
                'ordering': ['tech'],
            },
        ),
        migrations.AlterField(
            model_name='appliedby',
            name='tech',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.WorkByTech'),
        ),
        migrations.DeleteModel(
            name='TeamLinks',
        ),
    ]
