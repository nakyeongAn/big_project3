# Generated by Django 4.2 on 2024-01-11 06:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0008_three"),
    ]

    operations = [
        migrations.AlterField(
            model_name="three",
            name="three_products",
            field=models.TextField(blank=True, null=True),
        ),
    ]
