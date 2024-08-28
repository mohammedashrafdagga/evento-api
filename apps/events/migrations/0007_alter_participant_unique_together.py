# Generated by Django 5.1 on 2024-08-26 12:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_participant_join_datetime"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="participant",
            unique_together={("user", "event")},
        ),
    ]
