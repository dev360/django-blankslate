#coding=utf-8
from django.conf.urls.defaults import *
from django.utils.http import urlquote


from core import views

urlpatterns = patterns('',
	# Common views
	url(r'^$', views.index, name='index'),
	url(r'^profile/$', views.profile_index, name='profile-index'),
    url(r'^profile/edit/$', views.profile_edit, name='profile-edit'),
    url(r'^profile/users/$', views.users_index, name='users-index'),

    # Misc views
    url(r'^terms/$', views.terms_of_service, name='terms-of-service'),
    url(r'^privacy/$', views.privacy_policy, name='privacy-policy'),
)

