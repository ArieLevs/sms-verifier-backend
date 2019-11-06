
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contacts(models.Model):
    first_name = models.CharField(_('First Name'), max_length=255, null=False)
    last_name = models.CharField(_('Last Name'), max_length=255, null=True, default='')
    phone_number = models.CharField(_('Phone Number'), primary_key=True, max_length=32, null=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('contacts')
        verbose_name_plural = _('contacts')
        db_table = 'contacts'


class Event(models.Model):
    name = models.CharField(_('Event Name'), max_length=255, null=False)
    type = models.CharField(_('Event Type'), max_length=64, null=False)
    event_message_content = models.TextField(_('Message of Event'), null=False, blank=False)
    event_date = models.DateField(_('Events Date'), null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('event')
        db_table = 'event'


class EventAttendances(models.Model):
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE)
    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4)

    is_attending = models.BooleanField(_('Is Attending'), default=False)
    num_of_guests = models.IntegerField(_('Number of guests attending'), default=0)

    def __str__(self):
        return self.contact.first_name + ' ' + self.contact.last_name + ' - ' + str(self.uuid)

    class Meta:
        unique_together = (('event', 'contact'),)  # Set primary combined key
        verbose_name = _('event_attendances')
        verbose_name_plural = _('event_attendances')
        db_table = 'event_attendances'


class BroadcastList(models.Model):
    name = models.CharField(_('Name of List'), max_length=255, null=False,)
    for_event = models.OneToOneField(to=Event, on_delete=models.CASCADE)
    attendances = models.ManyToManyField(EventAttendances)

    class Meta:
        verbose_name = _('broadcast_list')
        verbose_name_plural = _('broadcast_list')
        db_table = 'broadcast_list'
