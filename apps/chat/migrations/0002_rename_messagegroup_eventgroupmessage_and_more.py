# Generated by Django 5.1 on 2024-09-29 10:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
        ("events", "0013_alter_event_category"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="MessageGroup",
            new_name="EventGroupMessage",
        ),
        migrations.RenameModel(
            old_name="MessageUsers",
            new_name="UserGroupMessage",
        ),
        migrations.RemoveField(
            model_name="eventgroupmessage",
            name="group",
        ),
        migrations.AddField(
            model_name="eventgroupmessage",
            name="event",
            field=models.ForeignKey(
                default=4,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="events.event",
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="ChatGroup",
        ),
    ]