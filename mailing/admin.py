from django.contrib import admin

from mailing.models import MessageMailing


@admin.register(MessageMailing)
class MessageMailingAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body')
    list_filter = ('mailing',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('status',)
