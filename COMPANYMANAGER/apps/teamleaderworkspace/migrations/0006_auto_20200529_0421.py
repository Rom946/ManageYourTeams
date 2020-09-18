# Generated by Django 3.0 on 2020-05-29 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0005_auto_20200529_0156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donetoday',
            options={'ordering': ['date_work']},
        ),
        migrations.AlterModelOptions(
            name='train',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='donetoday',
            name='date_work',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='donetoday',
            name='team_leader',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='partstocar',
            name='car',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]