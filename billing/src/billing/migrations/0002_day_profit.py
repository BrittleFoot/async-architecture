# Generated by Django 5.0 on 2024-03-08 23:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="day",
            name="profit",
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
