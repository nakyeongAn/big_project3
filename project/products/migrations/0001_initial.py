# Generated by Django 5.0 on 2024-01-09 04:07

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("category", models.CharField(blank=True, max_length=2000, null=True)),
                ("name", models.CharField(blank=True, max_length=2000, null=True)),
                ("price", models.IntegerField(blank=True, null=True)),
                ("grade", models.FloatField(blank=True, null=True)),
                ("product_url", models.URLField()),
                ("img_url", models.URLField()),
                ("category1", models.CharField(blank=True, max_length=2000, null=True)),
                ("category2", models.CharField(blank=True, max_length=2000, null=True)),
                ("category3", models.CharField(blank=True, max_length=2000, null=True)),
                ("red", models.IntegerField(blank=True, null=True)),
                ("green", models.IntegerField(blank=True, null=True)),
                ("blue", models.IntegerField(blank=True, null=True)),
                ("text", models.CharField(blank=True, max_length=2000, null=True)),
                ("embed", models.CharField(blank=True, max_length=2000, null=True)),
            ],
        ),
    ]
