from sms_verifier_app.models import Contacts
from django.contrib import admin


@admin.register(Contacts)
class CustomDevicesAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    ordering = ('first_name',)
    pass
