from sms_verifier_app.models import Contacts, BroadcastList, Event, EventAttendances
from django.contrib import admin


@admin.register(Contacts)
class CustomDevicesAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    ordering = ('first_name',)
    pass


@admin.register(BroadcastList)
class BroadcastListAdmin(admin.ModelAdmin):
    list_display = ('name', 'for_event')
    ordering = ('name',)
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date')
    ordering = ('name',)
    pass


@admin.register(EventAttendances)
class EventAttendancesAdmin(admin.ModelAdmin):
    list_display = ('contact', 'event', 'uuid')
    ordering = ('contact',)
    pass
