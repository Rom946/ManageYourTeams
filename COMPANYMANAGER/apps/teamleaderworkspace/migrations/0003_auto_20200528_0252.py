# Generated by Django 3.0 on 2020-05-28 00:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamleaderworkspace', '0002_auto_20200523_0430'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='abbreviation',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='possible_locations',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('L', 'Left'), ('R', 'Right'), ('1L', '1 Left'), ('2L', '2 Left'), ('3L', '3 Left'), ('4L', '4 Left'), ('5L', '5 Left'), ('6L', '6 Left'), ('1R', '1 Right'), ('2R', '2 Right'), ('3R', '3 Right'), ('4R', '4 Right'), ('5R', '5 Right'), ('6R', '6 Right'), ('NA', 'NA')], default='NA', max_length=10),
        ),
        migrations.AddField(
            model_name='reference',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='reference',
            name='qty_Mcar',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reference',
            name='qty_TCcar',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reference',
            name='surface',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='train',
            name='parts',
            field=models.ManyToManyField(to='teamleaderworkspace.Part'),
        ),
        migrations.AddField(
            model_name='train',
            name='references',
            field=models.ManyToManyField(to='teamleaderworkspace.Reference'),
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Train')),
            ],
        ),
        migrations.CreateModel(
            name='DoneToday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_work', models.DateField()),
                ('team', models.ManyToManyField(to='teamleaderworkspace.Tech')),
                ('team_leader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Train')),
            ],
        ),
        migrations.CreateModel(
            name='AppliedBy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DoneToday', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.DoneToday')),
                ('reference_applied', models.ManyToManyField(to='teamleaderworkspace.Reference')),
                ('tech', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Tech')),
            ],
        ),
    ]
