# Generated by Django 3.0 on 2020-07-22 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshopworkspace', '0009_auto_20200721_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockFilm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_record', models.DateField(auto_now=True)),
                ('qty', models.IntegerField(default=0)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshopworkspace.Film')),
            ],
        ),
        migrations.CreateModel(
            name='StockFilmHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateField(auto_now_add=True)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workshopworkspace.Film')),
                ('stock', models.ManyToManyField(to='workshopworkspace.StockFilm')),
            ],
        ),
    ]
