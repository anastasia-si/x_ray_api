# Generated by Django 3.0.5 on 2020-04-13 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('X_Ray_App', '0002_auto_20200413_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xray',
            name='image',
            field=models.ImageField(default=None, upload_to='xray_images/'),
        ),
    ]
