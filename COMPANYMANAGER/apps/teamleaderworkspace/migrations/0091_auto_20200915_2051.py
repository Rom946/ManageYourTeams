# Generated by Django 3.0 on 2020-09-15 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamleaderworkspace', '0090_auto_20200915_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='image',
            field=models.ImageField(default='train.png', upload_to='reference_pics'),
        ),
    ]