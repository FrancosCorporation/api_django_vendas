# Generated by Django 3.1.2 on 2020-11-01 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201101_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.TextField(max_length=60, unique=True),
        ),
    ]
