from django.contrib import admin
from .models import Ticket, TicketSeller


# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "event__id",
        "event__name",
        "ticket_price",
        "max_user",
    )


admin.site.register(Ticket, TicketAdmin)


# Ticket Admin Seller
class TicketSellerAdmin(admin.ModelAdmin):
    list_display = ("ticket__title", "buyer__username", "create_at")


admin.site.register(TicketSeller, TicketSellerAdmin)
