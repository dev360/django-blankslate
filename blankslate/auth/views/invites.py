#coding=utf-8

from django import http
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext

from auth.models import Profile, Organization, Address, Phonenumber
from auth.forms import UserInvitationForm


@login_required
def users_invite(request):
    users = []

    args = {}
    args['invite_user1_form'] = InviteUserForm()

    return render_to_response('auth/profiles/users_index.html', args, RequestContext(request))


