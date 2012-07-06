#coding=utf-8
from datetime import date
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


from auth.models import User, Profile, UserInvitation
from utils import forms


class UserInvitationForm(forms.ModelForm):
    """ This form is for adding/editing the profile """
    def __init__(self, *args, **kwargs):
        super(UserInvitationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = { 'placeholder': self.fields['first_name'].label }
        self.fields['last_name'].widget.attrs = { 'placeholder': self.fields['last_name'].label }
        self.fields['email'].widget.attrs = { 'placeholder': self.fields['email'].label }


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
    class Meta:
        model = UserInvitation
