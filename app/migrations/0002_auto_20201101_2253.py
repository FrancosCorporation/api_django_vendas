# Generated by Django 3.1.2 on 2020-11-01 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
