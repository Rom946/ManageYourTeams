# Generated by Django 3.0 on 2020-06-30 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0022_tech_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reference',
            name='part',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='selected',
        ),
        migrations.AddField(
            model_name='part',
            name='references',
            field=models.ManyToManyField(to='teamleaderworkspace.Reference'),
        ),
    ]