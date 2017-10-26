# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from marketplace.settings import MEDIA_URL
from marketplaceapp.models import Gig, Profile
from marketplaceapp.forms import GigForm

import marketplaceapp.braintree_config
import braintree

def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(
        request,
        'home.html',
        {'gigs': gigs, 'media_url': MEDIA_URL}
    )

def gig_details(request, id):
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect(home)

    client_token = braintree.ClientToken.generate()

    return render(
        request,
        'gig_details.html',
        {'gig': gig, 'client_token': client_token, 'media_url': MEDIA_URL}
    )

@login_required(login_url='/')
def create_gig(request):
    error = '' # Default msg value
    if request.method == 'POST':
        gig_form = GigForm(request.POST, request.FILES)
        if gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.user = request.user
            gig.save()
            return redirect(my_gigs)
        else:
            error = 'The data is not valid'

    gig_form = GigForm()

    return render(
        request,
        'create_gig.html',
        {'error': error}
    )

@login_required(login_url='/')
def edit_gig(request, id):
    try:
        gig = Gig.objects.get(id=id, user=request.user)
        error = '' # Default value

        if request.method == 'POST':
            gig_form = GigForm(request.POST, request.FILES, instance=gig)
            if gig_form.is_valid():
                gig.save()
                return redirect(my_gigs)
            else:
                error = 'The data is not valid'

        return render(
            request,
            'edit_gig.html',
            {'gig': gig, 'error': error, 'media_url': MEDIA_URL}
        )

    except Gig.DoesNotExist:
        return redirect(home)

@login_required(login_url='/')
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)

    return render(
        request,
        'my_gigs.html',
        {'gigs': gigs}
    )

@login_required(login_url='/')
def profile(request, username):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        __update_profile(request, profile)
    else:
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return redirect(home)

    gigs = Gig.objects.filter(user=profile.user, status=True)

    return render(
        request,
        'profile.html',
        {'profile': profile, 'gigs': gigs, 'media_url': MEDIA_URL}
    )

@login_required(login_url='/')
def create_purchase(request):
    if request.method == 'POST':
        try:
            gig_id = request.POST.get('gig_id')
            gig = Gig.objects.get(id=gig_id)
        except Gig.DoesNotExist:
            return redirect(home)

        nonce = request.POST.get('payment_method_nonce')
        result = braintree.Transaction.sale({
            'amount': gig_price,
            'payment_method_nonce': nonce
        })

        if result.is_success:
            print('Success!')
        else:
            print('Failed')

        return None
        return redirect(home)

def __update_profile(request, profile):
    profile.bio = request.POST.get('bio')
    profile.slogan = request.POST.get('slogan')
    profile.save()
