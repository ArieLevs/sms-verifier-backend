import os
import uuid

import datetime
import pytz
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sms_verifier_app.storage import OverwriteStorage


class Contacts(models.Model):
    first_name = models.CharField(_('First Name'), max_length=255, null=False)
    last_name = models.CharField(_('Last Name'), max_length=255, null=True, default='')
    phone_number = models.CharField(_('Phone Number'), primary_key=True, max_length=32, null=False)

    # set created date, and update field each time this model is updated
    created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Last Updated'), auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('contacts')
        verbose_name_plural = _('contacts')
        db_table = 'contacts'


# Return current event media directory
def user_media_directory_path(instance, filename):
    # Extract the file extension from the file
    file_name, file_extension = os.path.splitext(filename)

    # file will be uploaded to MEDIA_ROOT/event_<id>/<filename>
    return 'event_{0}/{1}'.format(instance.id, 'event_image' + str(file_extension))


class Event(models.Model):
    name = models.CharField(_('Event Name'), max_length=255, null=False)
    type = models.CharField(_('Event Type'), max_length=64, null=False)
    event_date = models.DateField(_('Events Date'), null=False)
    event_location_name = models.CharField(_('Event Location Name'), max_length=255, null=False)
    event_image = models.ImageField(max_length=255,
                                    storage=OverwriteStorage(),
                                    upload_to=user_media_directory_path,
                                    default='general_documents')
    waze_link = models.URLField(max_length=255, null=True, default=None)

    # set created date, and update field each time this model is updated
    created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Last Updated'), auto_now=True)

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

    is_responded = models.BooleanField(_('Is Responded'), default=False)
    date_responded = models.DateTimeField(_('Date Responded'), default=datetime.datetime(2019, 1, 1, 0, 0, 0),
                                          blank=True)
    is_attending = models.BooleanField(_('Is Attending'), default=False)

    # although this object has a single contacts foreign key,
    # an attendance can be for example, 'Alice and Bob Smith', or 'Alice and her partner',
    # this way the user will need to specify invited number
    num_of_invited = models.IntegerField(_('Number of guests invited'), default=0)
    num_of_attending = models.IntegerField(_('Number of guests attending'), default=0)

    # set created date, and update field each time this model is updated
    created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Last Updated'), auto_now=True)

    def __str__(self):
        return self.contact.first_name + ' ' + self.contact.last_name + ' - ' + str(self.uuid)

    def __init__(self, *args, **kwargs):
        super(EventAttendances, self).__init__(*args, **kwargs)
        self.__is_responded = self.is_responded

    def save(self, *args, **kwargs):
        # update the date_responded datetime field only when the is_responded field is set to True
        if self.is_responded and not self.__is_responded:
            self.date_responded = datetime.datetime.now(tz=pytz.utc)
        super(EventAttendances, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('event', 'contact'),)  # Set primary combined key
        verbose_name = _('event_attendances')
        verbose_name_plural = _('event_attendances')
        db_table = 'event_attendances'


class BroadcastList(models.Model):
    name = models.CharField(_('Name of List'), max_length=255, null=False)
    for_event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    event_message_content = models.TextField(_('Message of Event'), null=False, blank=False)
    attendances = models.ManyToManyField(EventAttendances)

    # set created date, and update field each time this model is updated
    created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Last Updated'), auto_now=True)

    class Meta:
        unique_together = (('name', 'for_event'),)  # Set primary combined key
        verbose_name = _('broadcast_list')
        verbose_name_plural = _('broadcast_list')
        db_table = 'broadcast_list'
'2019-01-01 00:00:00'