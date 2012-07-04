#coding=utf-8

from django import http
from django.db import transaction
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, RequestSite
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.conf import settings

from core.models import Profile
from core.forms import AuthenticationForm, RegistrationForm


def index(request):
    return render_to_response('core/index.html', {}, RequestContext(request))

@transaction.commit_on_success
def register(request):
    """ Registers a member """
    form = RegistrationForm()

    if request.method == 'POST':
        data = request.POST
        form = RegistrationForm(data)

        if form.is_valid():
            user = form.save() #profile_callback=Member.objects.profile_callback)
            profile = Profile(user=user)
            profile.save()
            return HttpResponseRedirect(reverse('register_success'))

    return render_to_response('core/auth/register.html', {
        'form': form,
    }, RequestContext(request))


def register_success(request):
    return render_to_response('core/auth/register_success.html', { }, RequestContext(request))


def logout(request):
    """ Logs out a user """
    logout_user(request)
    to = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(to)


def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- redirects to http://example.com should
            # not be allowed, but things like /view/?param=http://example.com
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            try:
                request.user.profile
            except Profile.DoesNotExist:
                profile = Profile(user=request.user, first_name='', last_name='')
                profile.save()

            return HttpResponseRedirect(redirect_to)

    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)

    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
