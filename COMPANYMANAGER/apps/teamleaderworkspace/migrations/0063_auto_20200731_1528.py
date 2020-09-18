# Generated by Django 3.0 on 2020-07-31 13:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0062_auto_20200730_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgressOnCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_on_car', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('finished', models.BooleanField(default=False)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Car')),
                ('jobs', models.ManyToManyField(to='teamleaderworkspace.Job')),
                ('progress_on_part', models.ManyToManyField(to='teamleaderworkspace.Part')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Train')),
            ],
        ),
        migrations.CreateModel(
            name='ProgressOnPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_on_part', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('finished', models.BooleanField(default=False)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Car')),
                ('jobs', models.ManyToManyField(to='teamleaderworkspace.Job')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Part')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Train')),
            ],
        ),
        migrations.CreateModel(
            name='ProgressOnTrain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_on_train', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('finished', models.BooleanField(default=False)),
                ('jobs', models.ManyToManyField(to='teamleaderworkspace.Job')),
                ('progress_on_car', models.ManyToManyField(to='teamleaderworkspace.ProgressOnCar')),
                ('progress_on_part', models.ManyToManyField(to='teamleaderworkspace.Part')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Train')),
            ],
        ),
        migrations.DeleteModel(
            name='Progress',
        ),
    ]