#coding=utf-8

from django.contrib.auth.views import password_change, password_reset
from django.conf.urls.defaults import *
from django.utils.http import urlquote


from core import views

urlpatterns = patterns('',

	# Registration
	url(r'^users/register/$', views.register, name='register'),
        url(r'^users/register/success/$', views.register_success, name='register_success',),
	url(r'^users/login/$', views.login, name='auth_login'),


	# Common views
	url(r'^$', views.index, name='index'),
	url(r'^profile/$', views.profile_index, name='profile-index'),
        url(r'^profile/edit/$', views.profile_edit, name='profile-edit'),
        url(r'^profile/users/$', views.users_index, name='users-index'),

        # Misc views
        url(r'^terms/$', views.terms_of_service, name='terms-of-service'),
        url(r'^privacy/$', views.privacy_policy, name='privacy-policy'),
)

