# Generated by Django 5.1 on 2024-08-26 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0009_waitinglist"),
    ]

    operations = [
        migrations.RenameField(
            model_name="waitinglist",
            old_name="request_date",
            new_name="request_datetime",
        ),
    ]
