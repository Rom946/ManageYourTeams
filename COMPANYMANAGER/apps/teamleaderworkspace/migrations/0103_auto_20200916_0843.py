# Generated by Django 3.0 on 2020-09-16 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0102_quality_had_stock_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quality',
            name='default_type',
        ),
        migrations.AddField(
            model_name='quality',
            name='default_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.WasteCategory'),
        ),
    ]
