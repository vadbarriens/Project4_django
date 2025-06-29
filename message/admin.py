from django.contrib import admin

from message.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    list_filter = ('subject',)
    search_fields = ('subject', 'body')
