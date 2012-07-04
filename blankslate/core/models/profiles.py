#coding=utf-8
import datetime, os, linecache
from os.path import join as pjoin

from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


from django.contrib.localflavor.us.models import USStateField, USPostalCodeField, \
        PhoneNumberField

from utils.models import GUIDModel


ADDRESS_TYPE_CHOICES = (
    ('MAILING', _('mailing')),
    ('BILLING', _('billing')),
    ('BUSINESS', _('business / home')),
)

PHONENUMBER_TYPE_CHOICES = (
    ('HOME', _('home')),
    ('BUSINESS', _('business (main)')),
    ('MOBILE', _('mobile')),
    ('FAX', _('fax')),
    ('TOLLFREE', _('tollfree')),
)


class Address(GUIDModel):
    """ Address object """

    address1 = models.CharField(_('Address 1'), max_length=128)
    address2 = models.CharField(_('Address 2'), max_length=128, null=True, blank=True)
    address3 = models.CharField(_('Address 3'), max_length=128, null=True, blank=True)
    state = USStateField()
    zip_code = models.CharField(_('Zip'), max_length=16)
    city = models.CharField(_('City'), max_length=32)
    type = models.CharField(_('Type'), max_length=16, choices=ADDRESS_TYPE_CHOICES, editable=False, blank=True)

    @classmethod
    def are_equal(cls, address1, address2):
        fields = ['address1', 'address2', 'address3', 'state', 'zip_code', 'city']

        value = True

        for field in fields:
            value = getattr(address1, field) == getattr(address2, field)
            if not value:
                break

        return value


    def copy_to(self, other_address):
        """
        Copies the values of this address to address passed in.
        """

        if other_address:
            other_address.address1 = self.address1
            other_address.address2 = self.address2
            other_address.address3 = self.address3
            other_address.state = self.state
            other_address.zip_code = self.zip_code
            other_address.city = self.city
            other_address.type = self.type

        return other_address

    class Meta:
        app_label = 'core'
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


class Phonenumber(GUIDModel):
    """ Phonenumber object """

    number = models.CharField(_('number'), max_length=16, null=True, blank=True)
    extension = models.CharField(_('extension'), max_length=8, null=True, blank=True)
    type = models.CharField(_('type'), max_length=16, choices= PHONENUMBER_TYPE_CHOICES, editable=False)

    @classmethod
    def valid_number(self, value):
        """ Determines if a phone number is valid. """

        stripped = ''.join([x for x in value if x.isdigit() or x.isalpha()])

        if len(stripped) == 11 and stripped[0] == '1':
            return True

        if len(stripped) == 10 and stripped[0] != '0':
            return True

        return False

    @classmethod
    def format(self, value):
        """ Formats the damned number. Nuf said. """

        stripped = ''.join([x for x in value if x.isdigit() or x.isalpha()])

        if not stripped:
            return ''

        # Make length eleven gud damn it.
        if len(stripped) == 10:
            stripped = '1{0}'.format(stripped)

        # From the horse's mouth:
        #
        #  http://www.fcc.gov/guides/toll-free-numbers-and-how-they-work
        #
        is_800 = stripped[:4] in ['1800', '1888', '1877', '1866', '1855']

        # Check to see if the number has alpha characters
        has_alpha = reduce( lambda acc, x: acc or x, [x.isalpha() for x in stripped])

        stripped = stripped.upper()

        if is_800 and has_alpha:
            # Do 1-800-FLOWERS style.
            return '{0}-{1}{2}{3}-{4}{5}{6}{7}{8}{9}{10}'.format(*stripped)

        if is_800 and not has_alpha:
            # Do 1-888-123-1234 style.
            return '{0}-{1}{2}{3}-{4}{5}{6}-{7}{8}{9}{10}'.format(*stripped)

        if not is_800 and has_alpha:
            # Do (305) GETCASH style.
            return '({1}{2}{3}) {4}{5}{6}{7}{8}{9}{10}'.format(*stripped)
        else:
            # Do (305) 123-1234
            return '({1}{2}{3}) {4}{5}{6}-{7}{8}{9}{10}'.format(*stripped)

    def save(self, *args, **kwargs):
        self.number = Phonenumber.format(self.number)
        super(Phonenumber, self).save(*args, **kwargs)

    class Meta:
        app_label = 'core'
        verbose_name = _('phone number')
        verbose_name_plural = _('phone numbers')


class Organization(GUIDModel):
    """ An organization """

    name = models.CharField(_('name'), max_length=64)
    email_domain = models.CharField(_('email domain'), max_length=255)

    members = models.ManyToManyField(User, verbose_name=_('approved_members'), related_name='member_organization')

    # billing_users = models.ManyToManyField(User, verbose_name=_('billing users'), related_name='billing_organizations')
    admin_users = models.ManyToManyField(User, verbose_name=_('admin users'), related_name='admin_organizations')
    users = models.ManyToManyField(User, verbose_name=_('users'), related_name='user_organizations')

    def __unicode__(self):
        return u'{0}'.format(self.name)

    class Meta:
        app_label = 'core'
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')


class ProfileManager(models.Manager):
    """ Manager for the profile object """

    def get_query_set(self):
        uber = super(ProfileManager, self)
        return uber.get_query_set().select_related('user')



PROFILE_STATUS_CHOICES = (
    ('NEW', _('New')),
    ('REG', _('Registered')),
)

class Profile(GUIDModel):
    """
    Profile object with some basic contact
    information.
    """
    status = models.CharField(_('status'), max_length=10, editable=False, default='NEW', choices=PROFILE_STATUS_CHOICES)
    user = models.OneToOneField(User, verbose_name=_('user'),
            related_name='profile', editable=False, unique=True)

    first_name = models.CharField(_('First Name'), null=True, max_length=128)
    last_name = models.CharField(_('Last Name'), null=True, max_length=128)
    middle_name = models.CharField(_('Middle Initial'), null=True, blank=True, max_length='64')
    company = models.CharField(_('Company Name'), max_length='255', null=True)

    addresses = models.ManyToManyField(Address, verbose_name=_('addresses'), related_name='profiles', blank=True)
    phone_numbers = models.ManyToManyField(Phonenumber, verbose_name=_('phone numbers'), related_name='profiles', blank=True)

    objects = ProfileManager()

    def save(self, **kwargs):
        if not self.id:
            self.slug = self.user.username

        super(Profile, self).save(**kwargs)

        # Save names to user as well.
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()

    @permalink
    def get_absolute_url(self):
        return ('profile-view', None, {'slug': self.slug})

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = 'core'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')


