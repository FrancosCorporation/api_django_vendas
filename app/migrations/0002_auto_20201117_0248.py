# Generated by Django 3.1.3 on 2020-11-17 02:48

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='permission',
            field=models.ForeignKey(default=app.models.Classificacao, on_delete=django.db.models.deletion.CASCADE, to='app.classificacao'),
        ),
    ]