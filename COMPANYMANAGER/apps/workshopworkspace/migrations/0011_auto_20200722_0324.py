# Generated by Django 3.0 on 2020-07-22 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0059_auto_20200721_1803'),
        ('workshopworkspace', '0010_stockfilm_stockfilmhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockfilmhistory',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshopworkspace.Film'),
        ),
        migrations.CreateModel(
            name='LayoutPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_of_ref_possible', models.IntegerField()),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshopworkspace.Film')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamleaderworkspace.Reference')),
            ],
        ),
    ]
