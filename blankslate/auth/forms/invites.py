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
        user = kwargs.pop('user', None)
        super(UserInvitationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = { 'placeholder': self.fields['first_name'].label }
        self.fields['last_name'].widget.attrs = { 'placeholder': self.fields['last_name'].label }
        self.fields['email'].widget.attrs = { 'placeholder': self.fields['email'].label }
        self.user = user

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
            raise forms.ValidationError(_('The user is already a member.'))

        except User.DoesNotExist:
            pass

        try:
            invitation = UserInvitation.objects.get(user=self.user, email__iexact=data)
            raise forms.ValidationError(_('You have already invited the user.'))

        except UserInvitation.DoesNotExist:
            pass

        return data

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        invitation = super(UserInvitationForm, self).save(*args, **kwargs)
        invitation.user = self.user
        invitation.save()
        return invitation


    class Meta:
        model = UserInvitation
