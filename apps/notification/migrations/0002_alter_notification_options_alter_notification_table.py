# Generated by Django 5.1 on 2024-10-22 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("notification", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={
                "verbose_name": "Notification",
                "verbose_name_plural": "Notifications",
            },
        ),
        migrations.AlterModelTable(
            name="notification",
            table="notifications",
        ),
    ]
