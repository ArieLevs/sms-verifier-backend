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
    list_display = ('contact', 'event', 'is_responded', 'date_responded', 'is_attending',)
    list_filter = ('is_responded', 'is_attending',)
    search_fields = ('contact__first_name', 'contact__last_name',)
    ordering = ('contact',)
    pass
