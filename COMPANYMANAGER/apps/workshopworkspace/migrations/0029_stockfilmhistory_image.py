# Generated by Django 3.0 on 2020-09-15 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshopworkspace', '0028_auto_20200807_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockfilmhistory',
            name='image',
            field=models.ImageField(default='photographic-film.png', upload_to='film_pics'),
        ),
    ]