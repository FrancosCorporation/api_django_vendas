# Initial schema for the existing application models.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ip",
            fields=[
                ("ip_address", models.GenericIPAddressField(primary_key=True, serialize=False)),
                ("count", models.IntegerField()),
                ("date_last_try", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Products",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ("nameproduct", models.CharField(max_length=100)),
                ("descripction", models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("email", models.EmailField(max_length=100, primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("last_login", models.DateTimeField()),
                ("date_auth", models.DateTimeField()),
                ("token", models.CharField(max_length=164, unique=True)),
                ("is_active", models.BooleanField(auto_created=True, default=False)),
                ("activate", models.BooleanField(auto_created=True, default=False)),
            ],
        ),
    ]
