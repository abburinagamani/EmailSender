

# Register your models here.
from django.contrib import admin
from .models import EmailLog

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['to_email', 'subject', 'status', 'sent_at']
    search_fields = ['to_email', 'subject', 'error_message']