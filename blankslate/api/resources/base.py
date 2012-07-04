from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized, HttpBadRequest, HttpForbidden
from tastypie.resources import ModelResource as BaseModelResource, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash


class DjangoAuthentication(Authentication):
    """ Basic django authentication """

    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()


    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username



class ModelResource(BaseModelResource):
    """ Model resource base class """

    pass

