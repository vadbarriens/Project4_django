from django.contrib import admin

from mailings.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('first_dispatch', 'status', 'message')
    list_filter = ('first_dispatch',)
    search_fields = ('status', 'message')
