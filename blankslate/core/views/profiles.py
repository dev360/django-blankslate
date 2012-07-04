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

from core.models import Profile, Organization, Address, Phonenumber
from core.forms import ProfileForm, AddressForm, PhonenumberForm



@login_required
def profile_index(request):

    profile = get_object_or_404(Profile, user=request.user)

    return render_to_response('core/profiles/index.html', {
        'profile': profile,
    }, RequestContext(request))


@login_required
def profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    return render_to_response('core/profiles/view.html', {'profile': profile}, RequestContext(request))


@login_required
def profile_add(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    return render_to_response('core/profiles/add.html', {'profile': profile, 'form': form}, RequestContext(request))


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user__id=request.user.id)

    #
    # Addresses
    #
    try:
        address1 = profile.addresses.filter(type='BUSINESS')[0]
    except IndexError:
        address1 = Address(type='BUSINESS')

    try:
        address2 = profile.addresses.filter(type='MAILING')[0]
    except IndexError:
        address2 = Address(type='MAILING')

    #
    # Phone numbers
    #
    try:
        phone1 = profile.phone_numbers.filter(type='BUSINESS')[0]
    except IndexError:
        phone1 = Phonenumber(type='BUSINESS')

    try:
        phone2 = profile.phone_numbers.filter(type='MOBILE')[0]
    except IndexError:
        phone2 = Phonenumber(type='MOBILE')

    try:
        phone3 = profile.phone_numbers.filter(type='FAX')[0]
    except IndexError:
        phone3 = Phonenumber(type='FAX')


    same_address = Address.are_equal(address1, address2)

    form = ProfileForm(instance=profile, initial={ 'same_address': same_address })

    # Address forms
    address1_form = AddressForm(prefix='physical_address', instance=address1)
    address2_form = AddressForm(prefix='mailing_address', instance=address2)

    # Phone forms
    phone1_form = PhonenumberForm(instance=phone1, prefix='phone1')
    phone2_form = PhonenumberForm(instance=phone2, prefix='phone2', always_valid=True)
    phone3_form = PhonenumberForm(instance=phone3, prefix='phone3', always_valid=True)

    certification, created = NotaryProfile.objects.get_or_create(profile=profile)
    certification_form = NotaryCertificationForm(instance=certification, initial={ 'profile': profile })

    saved = False
    validation_error = False

    if request.method == 'POST':
        data = request.POST

        form = ProfileForm(data, instance=profile)
        address1_form = AddressForm(data, prefix='physical_address', instance=address1)
        address2_form = AddressForm(data, prefix='mailing_address', instance=address2)

        phone1_form = PhonenumberForm(data, instance=phone1, prefix='phone1')
        phone2_form = PhonenumberForm(data, instance=phone2, prefix='phone2', always_valid=True)
        phone3_form = PhonenumberForm(data, instance=phone3, prefix='phone3', always_valid=True)

        if form.is_valid():
            same_address = form.cleaned_data['same_address']

            address1_valid = address1_form.is_valid()
            address2_valid = address1_valid if same_address else address2_form.is_valid()

            if address1_valid and address2_valid and phone1_form.is_valid() and phone2_form.is_valid() and phone3_form.is_valid():
                # Save profile.
                profile = form.save(user=request.user)

                # Save first one
                address1 = address1_form.save()

                if same_address:
                    address2 = address1.copy_to(address2)
                    address2.type = 'MAILING'
                    address2.save()

                    # Dont forget to update the damned form. Notice no data
                    address2_form = AddressForm(prefix='mailing_address', instance=address2)

                else:
                    address2 = address2_form.save()

                if address1 not in profile.addresses.all():
                    profile.addresses.add(address1)

                if address2 not in profile.addresses.all():
                    profile.addresses.add(address2)

                phone1 = phone1_form.save()

                if phone1 not in profile.phone_numbers.all():
                    profile.phone_numbers.add(phone1)

                if phone2_form.is_valid():
                    phone2 = phone2_form.save()
                    if phone2 not in profile.phone_numbers.all():
                        profile.phone_numbers.add(phone2)
                else:
                    if phone2 in profile.phone_numbers.all():
                        profile.phone_numbers.remove(phone2)

                if phone3_form.is_valid():
                    phone3 = phone3_form.save()
                    if phone3 not in profile.phone_numbers.all():
                        profile.phone_numbers.add(phone3)
                else:
                    if phone3 in profile.phone_numbers.all():
                        profile.phone_numbers.remove(phone3)


                profile.save()
                saved = True

                # Check if users addresses are actually the same, in that
                # case we should force the same addresses button to be checked.
                same_address = Address.are_equal(address1, address2)
                form = ProfileForm(instance=profile, initial={ 'same_address': same_address })

                phone2_data = data if phone2_form.is_valid else None
                phone3_data = data if phone3_form.is_valid else None

                phone1_form = PhonenumberForm(instance=phone1, prefix='phone1')
                phone2_form = PhonenumberForm(instance=phone2, prefix='phone2', always_valid=True)
                phone3_form = PhonenumberForm(instance=phone3, prefix='phone3', always_valid=True)

            else:
                validation_error = True
        else:
            validation_error = True

    args = {}
    args['profile'] = profile
    args['form'] = form
    args['phone1_form'] = phone1_form
    args['phone2_form'] = phone2_form
    args['phone3_form'] = phone3_form
    args['address1_form'] = address1_form
    args['address2_form'] = address2_form
    args['certification_form'] = certification_form

    args['saved'] = saved
    args['validation_error'] = validation_error
    return render_to_response('core/profiles/edit.html', args, RequestContext(request))


@login_required
def profile_search(request):
    profiles = []
    return render_to_response('core/index.html', {'profiles': profiles}, RequestContext(request))



def users_index(request):
    users = []

    args = {}
    args['invite_user1_form'] = InviteUserForm()

    return render_to_response('core/profiles/users_index.html', args, RequestContext(request))

