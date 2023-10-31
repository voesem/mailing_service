from django.contrib import admin

from mailing.models import Client, Mailing, Message, Log

admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Log)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    ordering = ('id',)
