# Generated by Django 5.1 on 2024-08-22 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_remove_event_date_event_background_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="section",
            name="location",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
