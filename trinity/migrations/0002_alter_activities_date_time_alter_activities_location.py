# Generated by Django 5.0.6 on 2024-06-21 01:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trinity", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activities",
            name="date_time",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="activities",
            name="location",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
