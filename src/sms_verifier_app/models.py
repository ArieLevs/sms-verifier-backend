
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contacts(models.Model):
    first_name = models.CharField(_('First Name'), max_length=255, null=False)
    last_name = models.CharField(_('Last Name'), max_length=255, null=True, default='')
    phone_number = models.CharField(_('Phone Number'), primary_key=True, max_length=32, null=False)
    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4)

    class Meta:
        verbose_name = _('contacts')
        verbose_name_plural = _('contacts')
        db_table = 'contacts'
