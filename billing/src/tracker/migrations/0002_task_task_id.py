# Generated by Django 5.0 on 2024-03-09 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_id',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
