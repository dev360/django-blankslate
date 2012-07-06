#coding=utf-8

from django.contrib.auth.views import password_change, password_reset
from django.conf.urls.defaults import *
from django.utils.http import urlquote


from auth import views

urlpatterns = patterns('',

	# Registration
	url(r'^register/$', views.register, name='register'),
    url(r'^register/success/$', views.register_success, name='register_success',),
	url(r'^activate/$', views.activate, name='activate'),
	url(r'^activate/success/$', views.activate_success, name='activate_success'),

    # Login / logout
    url(r'^login/$', views.login, name='auth_login'),
    url(r'^logout/$', views.logout, name='auth_logout'),

    # Password reset
    url(r'^password/reset/$', views.password_reset, name='password_reset'),
    url(r'^password/form/$', views.password_form, name='password_reset_form'),


    # Invitations

    # User management

)


