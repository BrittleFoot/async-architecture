# Generated by Django 5.0 on 2024-03-10 11:29

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                (
                    "profit",
                    models.DecimalField(decimal_places=0, default=0, max_digits=10),
                ),
                (
                    "public_id",
                    models.IntegerField(db_index=True, editable=False, unique=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                (
                    "public_id",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("bad_luck", "Bad Luck"),
                            ("earning", "Earning"),
                            ("payment", "Payment"),
                        ],
                        max_length=255,
                    ),
                ),
                ("comment", models.TextField()),
                (
                    "credit",
                    models.DecimalField(
                        decimal_places=0, default=0, editable=False, max_digits=10
                    ),
                ),
                (
                    "debit",
                    models.DecimalField(
                        decimal_places=0, default=0, editable=False, max_digits=10
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
