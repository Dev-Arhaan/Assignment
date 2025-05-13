from django.contrib import admin

# Register your models here.
from .models import Reminder

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('reminder_datetime', 'message', 'reminder_method', 'created_at')
    list_filter = ('reminder_method', 'reminder_datetime')
    search_fields = ('message',)