# Generated by Django 5.0 on 2024-01-10 11:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accountuser",
            name="gender",
            field=models.CharField(
                choices=[("여자", "여자"), ("남자", "남자")], default="남자", max_length=3
            ),
        ),
    ]
