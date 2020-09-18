# Generated by Django 3.0 on 2020-05-28 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0004_auto_20200528_0417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='parts',
        ),
        migrations.RemoveField(
            model_name='train',
            name='references',
        ),
        migrations.AddField(
            model_name='train',
            name='date_started',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='train',
            name='last_modified',
            field=models.DateField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='partstocar',
            name='parts',
        ),
        migrations.AddField(
            model_name='partstocar',
            name='parts',
            field=models.ManyToManyField(to='teamleaderworkspace.Part'),
        ),
        migrations.CreateModel(
            name='RefsToCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Car')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Part')),
                ('references', models.ManyToManyField(to='teamleaderworkspace.Reference')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='teamleaderworkspace.Train')),
            ],
        ),
    ]