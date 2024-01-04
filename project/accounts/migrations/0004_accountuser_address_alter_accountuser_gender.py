# Generated by Django 5.0 on 2024-01-04 00:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_accountuser_agearound"),
    ]

    operations = [
        migrations.AddField(
            model_name="accountuser",
            name="address",
            field=models.CharField(default="None", max_length=100),
        ),
        migrations.AlterField(
            model_name="accountuser",
            name="gender",
            field=models.CharField(
                choices=[("여자", "여자"), ("남자", "남자")], default="남자", max_length=3
            ),
        ),
    ]