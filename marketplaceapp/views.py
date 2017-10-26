# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from marketplace.settings import MEDIA_URL
from marketplaceapp.models import Gig, Profile, Purchase, Review
from marketplaceapp.forms import GigForm

from marketplaceapp.braintree_config import braintree_init
import braintree

def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(
        request,
        'home.html',
        {'gigs': gigs, 'media_url': MEDIA_URL}
    )

def gig_details(request, id):
    if request.method == 'POST' and \
        not request.user.is_anonymous() and \
        Purchase.objects.filter(gig_id=id, buyer=request.user).count() > 0 and \
        'content' in request.POST and \
        request.POST.get('content').strip() != '':
            Review.objects.create(
                content=request.POST.get('content'),
                gig_id=id,
                user=request.user
            )

    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect(home)

    if request.user.is_anonymous() or \
        Purchase.objects.filter(gig_id=id, buyer=request.user).count() == 0 or \
        Purchase.objects.filter(gig_id=id, user=request.user).count() > 0:
            show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(gig=gig, buyer=request.user).count() > 0

    reviews = Review.objects.filter(gig=gig)
    client_token = '' # Default value
    if request.user.is_anonymous():
        braintree_init()
        client_token = braintree.ClientToken.generate()

    return render(
        request,
        'gig_details.html',
        {'gig': gig, 'show_post_review': show_post_review, 'reviews': reviews, 'client_token': client_token, 'media_url': MEDIA_URL}
    )

@login_required(login_url=home)
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

@login_required(login_url=home)
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

@login_required(login_url=home)
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)

    return render(
        request,
        'my_gigs.html',
        {'gigs': gigs}
    )

@login_required(login_url=home)
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

@login_required(login_url=home)
def create_purchase(request):
    if request.method == 'POST':
        braintree_init()

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
            Purchase.objects.create(gig=gig, buyer=request.user)

        return redirect(home)

@login_required(login_url=home)
def my_sales(request):
    purchases = Purchase.objects.filter(gig__user=request.user)

    return render(
        request,
        'my_sales.html',
        {'purchases': purchases}
    )

@login_required(login_url=home)
def my_purchases(request):
    purchases = Purchase.objects.filter(buyer=request.user)

    return render(
        request,
        'my_purchases.html',
        {'purchases': purchases}
    )

def category(request, name):
    categories = {
        'scripts-software': 'SS',
        'graphics-design': 'GD',
        'web-marketing': 'WM',
        'videos': 'V',
        'music': 'M'
    }

    try:
        gigs = Gig.objects.filter(category=categories[name])

        return render(
            request,
            'home.html',
            {'gigs': gigs, 'media_url': MEDIA_URL}
        )
    except KeyError:
        return redirect(home)

def search(request):
    """Our Search form easy thanks Django ORM and title__contains"""
    gigs = Gig.objects.filter(title__contains=request.GET.get('title'))

    return render(
        request,
        'home.html',
        {'gigs': gigs, 'media_url': MEDIA_URL}
    )

def __update_profile(request, profile):
    profile.bio = request.POST.get('bio')
    profile.slogan = request.POST.get('slogan')
    profile.save()
