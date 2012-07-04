#coding=utf-8
from django.conf.urls.defaults import *

from tastypie.api import Api

from api import resources

v1_api = Api(api_name='1.0')
v1_api.register(resources.ProfileResource())
#v1_api.register(resources.PhonenumberResource())
#v1_api.register(resources.AddressResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)

