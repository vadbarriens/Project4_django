from django.contrib import admin
from recipient.models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    list_filter = ('comment',)
    search_fields = ('full_name', )
