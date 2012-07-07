#coding=utf-8

from django.contrib.auth import views as auth_views
from django.conf.urls.defaults import *
from django.utils.http import urlquote


from auth import views

urlpatterns = patterns('',

	# Registration
	url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/success/$', views.register_success, name='register_success',),
	url(r'^accounts/activate/(?P<activation_key>([^/])+)/$', views.activate, name='activate'),
	url(r'^accounts/activate/success/$', views.activate_success, name='activate_success'),

    # Login / logout
    # Dont change these paths.. it will break.
    url(r'^accounts/login/$', views.login, name='auth_login'),
    url(r'^accounts/logout/$', views.logout, name='auth_logout'),

    # Password reset stuff
    url(r'^password/change/$',
        auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),


    # Profiles
    url(r'^profile/$', views.profile_index, name='profile-index'),
    url(r'^profile/edit/$', views.profile_edit, name='profile-edit'),
    url(r'^profile/contact/edit/$', views.profile_contact_edit, name='profile-contact-edit'),

    # User management
    url(r'^profile/users/$', views.users_index, name='users-index'),
    url(r'^profile/users/invitations/$', views.users_invites, name='users-invites'),

)


