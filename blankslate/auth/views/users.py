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
def users_index(request):
    users = []

    args = dict(users = users)
    return render_to_response('auth/users/users_index.html', args, RequestContext(request))



@login_required
def users_invites(request):

    created = False

    users = []
    args = {}
    invite_form1 = UserInvitationForm(user=request.user)

    if request.method == 'POST':
        invite_form1 = UserInvitationForm(request.POST, user=request.user)

        if invite_form1.is_valid():
            invite_form1.save()
            invite_form1 = UserInvitationForm(user=request.user)

    args['invite_form1'] = invite_form1
    return render_to_response('auth/users/users_invites.html', args, RequestContext(request))

