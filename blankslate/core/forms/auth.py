#coding=utf-8
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.forms.widgets import Select


from registration.forms import RegistrationFormUniqueEmail
from core.models import User, Profile
from utils import forms


class PasswordField(forms.CharField):
    max_length=100
    widget=forms.PasswordInput()


class SessionMixin(object):
    def clean(self):
        result = super(SessionMixin, self).clean()
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't "
                    "appear to have cookies enabled. Cookies are required "
                    "for logging in."))
        return result

MEMBERTYPE_CHOICES = (
    ('', _('Select a member type')),
    # Add more as needed.
)

class RegistrationForm(forms.FormMixin, RegistrationFormUniqueEmail):

    # member_type = forms.CharField(label=_('Member type'), max_length=10, widget=Select(choices=MEMBERTYPE_CHOICES))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _('Username')
        self.fields['email'].label = _('Email address')
        self.fields['password1'].label = _('Password')
        self.fields['password2'].label = _('Password (again)')
        accepted_terms = forms.BooleanField(label=mark_safe(u'I accept the '
            u'<a href="/terms/">terms and conditions</a>'), required=True)

    def clean_username(self):
        data = self.cleaned_data['username']

        if User.objects.filter(username__iexact=data).exists():
            raise forms.ValidationError(u'This username is already taken.')

        return data

    def clean_email(self):
        data = self.cleaned_data['email']

        if User.objects.filter(email__iexact=data).exists():
            raise forms.ValidationError(u'Another user is registered with this email.')

        return data

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password1 != password2:
            raise forms.ValidationError(u'Your password did not match.')

        return password2


    def save(self, *args, **kwargs):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(username, email, password)
        profile, created = Profile.objects.get_or_create(user=user)


    class Meta:
        fields = ['email', 'password1', 'password2']



class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = forms.EmailField(label=_("Email"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if not user:
                raise forms.ValidationError(_("Please enter a correct email and password. Note that both fields are case-sensitive."))

            self.user_cache = authenticate(username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct email and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
