import logging
import simplejson

from django.conf.urls.defaults import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse

from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized, HttpBadRequest, HttpForbidden
from tastypie.resources import ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash

from .base import ModelResource, DjangoAuthentication

from auth.models import Profile, Address, Phonenumber

log = logging.getLogger(__name__)  # Get an instance of a logger


class ProfileResource(ModelResource):
    """ Profile resource """

    def get_resource_uri(self, bundle_or_obj):
        # Need this to return properly

        kwargs = { 'resource_name': self._meta.resource_name }

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        url =  reverse('api_profile_detail', kwargs=kwargs)
        log.debug('get_resource_uri: %s' % url)
        return url

    def base_urls(self):
        return []  # Wipe out the base urls.. were not going to use them.

    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_profile_detail"),
            ]

    def dispatch_detail(self, request, **kwargs):
        if request.method == 'PUT':
            return self.put_detail(request, **kwargs)

        return super(ProfileResource, self).dispatch_detail(request, **kwargs)

    def obj_get_detail(self, request, **kwargs):

        return Profile.objects.get(user_id=request.user.id)

    def put_detail(self, request, **kwargs):

        return super(ProfileResource, self).put_detail(request, **kwargs)

    def obj_update(self, bundle, request, **kwargs):
        profile_id = bundle.data.get('id')
        profile = Profile.objects.get(pk=profile_id)

        # Override this method to add additional validation
        if profile.user != request.user:
            raise ImmediateHttpResponse(response=HttpForbidden())

        return super(ProfileResource, self).obj_update(bundle, request, **kwargs)

    class Meta:
        resource_name = 'account/profile'
        queryset = Profile.objects.all()
        detail_allowed_methods = ['get', 'put',]
        authentication = DjangoAuthentication()

