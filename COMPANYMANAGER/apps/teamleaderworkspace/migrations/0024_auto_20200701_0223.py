# Generated by Django 3.0 on 2020-07-01 00:23

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0023_auto_20200630_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workdone',
            name='references_applied',
        ),
        migrations.AlterField(
            model_name='reference',
            name='possible_locations',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('L', 'Left'), ('R', 'Right'), ('1L', '1 Left'), ('2L', '2 Left'), ('3L', '3 Left'), ('4L', '4 Left'), ('5L', '5 Left'), ('6L', '6 Left'), ('1R', '1 Right'), ('2R', '2 Right'), ('3R', '3 Right'), ('4R', '4 Right'), ('5R', '5 Right'), ('6R', '6 Right'), ('NA', 'NA')], default='NA', max_length=100),
        ),
        migrations.DeleteModel(
            name='AppliedBy',
        ),
    ]
