# Generated by Django 3.0 on 2020-09-15 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshopworkspace', '0031_auto_20200915_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='image',
            field=models.ImageField(default='photographic-film.png', upload_to='film_pics'),
        ),
    ]
