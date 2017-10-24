# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from marketplace.settings import MEDIA_URL
from marketplaceapp.models import Gig
from marketplaceapp.forms import GigForm

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

    return render(
        request,
        'gig_details.html',
        {'gig': gig, 'media_url': MEDIA_URL}
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
    return render(
        request,
        'edit_gog.html',
        {}
    )

@login_required(login_url='/')
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)

    return render(
        request,
        'my_gigs.html',
        {'gigs': gigs}
    )
