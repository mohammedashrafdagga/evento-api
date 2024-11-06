# Generated by Django 5.1 on 2024-10-22 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ticket", "0003_alter_ticket_title"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ticket",
            options={"verbose_name": "Ticket", "verbose_name_plural": "Tickets"},
        ),
        migrations.AlterModelOptions(
            name="ticketseller",
            options={
                "verbose_name": "TicketSeller",
                "verbose_name_plural": "TicketSellers",
            },
        ),
        migrations.AlterModelTable(
            name="ticket",
            table="tickets",
        ),
        migrations.AlterModelTable(
            name="ticketseller",
            table="ticket_seller",
        ),
    ]