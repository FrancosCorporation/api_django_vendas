# Generated by Django 3.1.3 on 2020-11-17 02:44

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classificacao',
            fields=[
                ('delete', models.BooleanField(auto_created=True, default=False)),
                ('update', models.BooleanField(auto_created=True, default=False)),
                ('create', models.BooleanField(auto_created=True, default=False)),
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('ip_address', models.GenericIPAddressField(primary_key=True, serialize=False)),
                ('count', models.IntegerField()),
                ('date_last_try', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('activate', models.BooleanField(auto_created=True, default=False)),
                ('is_active', models.BooleanField(auto_created=True, default=False)),
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField()),
                ('date_auth', models.DateTimeField()),
                ('token', models.TextField(max_length=164, unique=True)),
                ('group', models.CharField(default='padrao', max_length=15)),
                ('session', models.CharField(default='', max_length=100)),
                ('permission', models.OneToOneField(default=app.models.Classificacao, on_delete=django.db.models.deletion.CASCADE, to='app.classificacao')),
            ],
        ),
    ]
