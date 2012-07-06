#coding=utf-8
import hashlib
import random
import datetime, os, linecache
from os.path import join as pjoin

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from utils.models import GUIDModel


class UserInvitation(GUIDModel):
    """ User invitation object """
    user = models.ForeignKey(User, verbose_name=_('user'), editable=False)
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=16)
    email = models.EmailField(_('email'))


    class Meta:
        app_label = 'core'
        verbose_name = _('address')
        verbose_name_plural = _('addresses')



