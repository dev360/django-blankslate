#coding=utf-8
from datetime import date
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


from core.models import User, Profile, Address, Phonenumber
from utils import forms


class ProfileForm(forms.ModelForm):
    """ This form is for adding/editing the profile """

    same_address = forms.BooleanField(label=_(u'Mailing address is the same as the physical address.'), required=False,)


    def save(self, user=None):
        if not user:
            raise Exception("User has to be specified")

        if not self.is_valid():
            raise Exception("Form has to be valid before saving")

        profile = Profile.objects.get(user=user)

        data = self.cleaned_data

        profile.first_name = data['first_name']
        profile.last_name = data['last_name']
        profile.middle_name = data['middle_name']
        profile.company = data['company']
        profile.save()

        return profile

    class Meta:
        model = Profile


class AddressForm(forms.ModelForm):
    """ Address form """

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Address


class PhonenumberForm(forms.ModelForm):
    """ Phonenumber form """

    def __init__(self, *args, **kwargs):

        self.always_valid = kwargs.pop('always_valid', False)

        super(PhonenumberForm, self).__init__(*args, **kwargs)

        type = self.instance.type if self.instance else None
        label = _('Phone')

        if type == 'BUSINESS':
            label = _('Main Number')
        elif type == 'MOBILE':
            label = _('Cell Number')
        elif type == 'FAX':
            label = _('Fax Number')

        self.fields['extension'].label = mark_safe('&nbsp;')
        self.fields['number'].label = _(label)
        self.fields['number'].required = not self.always_valid


    def clean_number(self):
        data = self.cleaned_data['number']
        if data and not Phonenumber.valid_number(data):
            raise forms.ValidationError(_('Invalid phone number'))

        return data


    class Meta:
        model = Phonenumber


class InviteUserForm(forms.Form):
    """ Form for inviting users """

    first_name = forms.CharField(label=_('First Name'), max_length=128, required=False)
    last_name = forms.CharField(label=_('Last Name'), max_length=128, required=False)
    email = forms.CharField(label=_('Email'), max_length=255)

    def clean_email(self):
        data = self.cleaned_data['email']

        try:
            user = User.objects.get(email__iexact=data)

            try:
                user_organization = user.user_organizations.all()[0]
            except IndexError:
                user_organization = None

            try:
                your_organization = request.user.user_organizations.all()[0]
            except IndexError:
                your_organization = None

            if user_organization and user_organization == your_organization:
                raise forms.ValidationError(_('The user is already in your organization.'))
            else:
                raise forms.ValidationError(_('The user already belongs to another organization.'))

        except User.DoesNotExist:
            return data

