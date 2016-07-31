from __future__ import unicode_literals

from django.db import models
import re

from django.contrib.auth.models import User

# Create your models here.


class TelegramChat(models.Model):
    chat_id = models.CharField(max_length=256, blank=False, null=False, unique=True)
    username = models.CharField(max_length=256, blank=False, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        # return unicode(self.user)
        return '%s %s' % (self.chat_id, self.username)