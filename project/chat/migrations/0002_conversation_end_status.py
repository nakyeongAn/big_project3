# Generated by Django 5.0 on 2024-01-08 06:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="end_status",
            field=models.BooleanField(default=False),
        ),
    ]