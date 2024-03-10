# Generated by Django 5.0 on 2024-03-10 11:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tracker", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="performer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tasks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
